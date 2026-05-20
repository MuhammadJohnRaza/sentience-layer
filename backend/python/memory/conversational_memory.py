"""
Conversational Memory Manager — Multi-Tier Redis Cache & Summary Compression.
Manages episodic chat queues and merges older contexts into semantic summaries.
"""
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ConversationalMemoryManager:
    """
    Manages dual-tier conversational memory:
      - Short-term sliding window inside Redis list structure.
      - Summarization trigger when active message lengths exceed thresholds.
    """
    def __init__(self, redis_client: Any, max_messages: int = 12):
        self.redis = redis_client
        self.max_messages = max_messages

    def _get_key(self, session_id: str) -> str:
        return f"session:memory:{session_id}"

    def _get_summary_key(self, session_id: str) -> str:
        return f"session:summary:{session_id}"

    def get_context(self, session_id: str) -> Dict[str, Any]:
        """Retrieves raw history list and current high-level summary from Redis."""
        if not self.redis:
            return {"summary": "", "history": []}
            
        try:
            key = self._get_key(session_id)
            summary_key = self._get_summary_key(session_id)
            
            # Fetch lists from Redis
            messages = [json.loads(m.decode("utf-8") if isinstance(m, bytes) else m) 
                        for m in self.redis.lrange(key, 0, -1)]
            summary_val = self.redis.get(summary_key)
            summary = summary_val.decode("utf-8") if isinstance(summary_val, bytes) else (summary_val or "")
            
            return {
                "summary": summary,
                "history": messages[::-1]  # chronologically sorted
            }
        except Exception as e:
            logger.warning(f"Failed to fetch conversation context from Redis: {e}")
            return {"summary": "", "history": []}

    def append_message(self, session_id: str, role: str, content: str, metadata: Dict[str, Any] = None):
        """Appends a conversation message and prunes lists that exceed self.max_messages."""
        if not self.redis:
            return
            
        try:
            key = self._get_key(session_id)
            message_data = {
                "role": role,
                "content": content,
                "metadata": metadata or {}
            }
            self.redis.lpush(key, json.dumps(message_data))
            self.redis.ltrim(key, 0, self.max_messages - 1)
        except Exception as e:
            logger.warning(f"Failed to append message to Redis memory: {e}")

    async def trigger_summarization(self, session_id: str, client_generator_fn) -> str:
        """
        Compresses older blocks of dialogue and merges them into the running semantic summary.
        Prevents conversational drift and context window overflows.
        """
        if not self.redis:
            return ""
            
        try:
            key = self._get_key(session_id)
            summary_key = self._get_summary_key(session_id)
            
            messages = [json.loads(m.decode("utf-8") if isinstance(m, bytes) else m) 
                        for m in self.redis.lrange(key, 0, -1)]
            
            if len(messages) < self.max_messages:
                return ""

            # Compress oldest 50%
            older_messages = messages[len(messages)//2:]
            summary_context = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in reversed(older_messages))
            
            prompt = f"""Summarize the key decisions, technical metrics, and open action items in this conversation history.
Maintain specific numeric data points (URLs, ROI percentages, latency times, IP addresses):
---
{summary_context}
---
Summary:"""
            
            new_summary = await client_generator_fn(prompt)
            if hasattr(new_summary, 'content'):
                new_summary = new_summary.content
            elif hasattr(new_summary, 'data') and isinstance(new_summary.data, dict):
                new_summary = new_summary.data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            new_summary = str(new_summary).strip()
            
            # Retrieve existing summary to merge
            existing_summary_val = self.redis.get(summary_key)
            existing_summary = existing_summary_val.decode("utf-8") if isinstance(existing_summary_val, bytes) else existing_summary_val
            
            if existing_summary:
                merge_prompt = f"""Merge these two summary logs into a single coherent paragraph.
Maintain all core metrics, entities, and priorities:
Summary A: {existing_summary}
Summary B: {new_summary}
Merged Summary:"""
                merged = await client_generator_fn(merge_prompt)
                if hasattr(merged, 'content'):
                    new_summary = merged.content
                elif hasattr(merged, 'data') and isinstance(merged.data, dict):
                    new_summary = merged.data.get('choices', [{}])[0].get('message', {}).get('content', '')
                new_summary = str(new_summary).strip()
                
            self.redis.set(summary_key, new_summary)
            
            # Trim the list in Redis
            self.redis.ltrim(key, 0, len(messages)//2)
            return new_summary
        except Exception as e:
            logger.warning(f"Failed memory consolidation: {e}")
            return ""
