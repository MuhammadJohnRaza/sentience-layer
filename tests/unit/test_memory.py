"""
Unit tests for the Conversational Memory Manager and Layout-Aware PDF Parser.
Verifies message persistence, queue trimming, summary trigger, and PDF structural analysis.
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.python.memory.conversational_memory import ConversationalMemoryManager
from backend.python.parser_wrapper import LayoutAwarePDFParser

# Mock Redis class for test scenarios
class FakeRedis:
    def __init__(self):
        self.store = {}
        
    def lrange(self, key, start, end):
        lst = self.store.get(key, [])
        # Simplified slicing
        return lst[start:] if end == -1 else lst[start:end+1]
        
    def lpush(self, key, val):
        if key not in self.store:
            self.store[key] = []
        self.store[key].insert(0, val)
        
    def ltrim(self, key, start, end):
        if key in self.store:
            self.store[key] = self.store[key][start:end+1]
            
    def get(self, key):
        return self.store.get(key, None)
        
    def set(self, key, val):
        self.store[key] = val if isinstance(val, bytes) else str(val).encode("utf-8")

def test_conversational_memory_manager_append_and_trim():
    fake_redis = FakeRedis()
    manager = ConversationalMemoryManager(fake_redis, max_messages=4)
    
    session_id = "test_sess_123"
    
    # 1. Test append messages
    manager.append_message(session_id, "user", "Message 1")
    manager.append_message(session_id, "assistant", "Response 1")
    manager.append_message(session_id, "user", "Message 2")
    manager.append_message(session_id, "assistant", "Response 2")
    
    ctx = manager.get_context(session_id)
    assert len(ctx["history"]) == 4
    assert ctx["history"][0]["content"] == "Message 1"
    assert ctx["history"][3]["content"] == "Response 2"
    
    # 2. Test trimming bounds
    manager.append_message(session_id, "user", "Message 3 (should trim)")
    ctx_trimmed = manager.get_context(session_id)
    assert len(ctx_trimmed["history"]) == 4
    # The oldest message (Message 1) should be pruned
    assert ctx_trimmed["history"][0]["content"] == "Response 1"

@pytest.mark.asyncio
async def test_conversational_memory_summarization():
    fake_redis = FakeRedis()
    manager = ConversationalMemoryManager(fake_redis, max_messages=4)
    session_id = "test_sess_456"
    
    manager.append_message(session_id, "user", "Project Alpha setup instructions")
    manager.append_message(session_id, "assistant", "Step 1 is cloning the repo")
    manager.append_message(session_id, "user", "Step 2 is config setup")
    manager.append_message(session_id, "assistant", "Ready to start")
    
    # Mock LLM generation call
    mock_llm = AsyncMock(return_value="Summary: Project Alpha repo clone and configuration setup initiated.")
    
    new_summary = await manager.trigger_summarization(session_id, mock_llm)
    
    assert "Alpha" in new_summary
    ctx = manager.get_context(session_id)
    # The history list should be trimmed to half its length
    assert len(ctx["history"]) == 2
    assert ctx["summary"] == "Summary: Project Alpha repo clone and configuration setup initiated."

def test_layout_pdf_parser_fallback():
    # Test parser behavior with plain text or missing dependencies
    parser = LayoutAwarePDFParser(b"%PDF-1.4 mock content", filename="mock.pdf")
    parse_result = parser.parse()
    
    # Verify standard metadata and structured output defaults
    assert "metadata" in parse_result
    assert parse_result["metadata"]["title"] == "mock.pdf"
    assert "sections" in parse_result
