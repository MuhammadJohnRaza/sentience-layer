"""
Swarm Orchestrator — 3-Agent Handoff Chain
Critic Agent → Consensus Agent → Action Playbook Agent

This is the core multi-agent reasoning pipeline.
Each agent receives the previous agent's output as structured context.
"""
import time
import json
import re
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

try:
    from antigravity_client import get_antigravity_client
except ImportError:
    from backend.python.antigravity_client import get_antigravity_client


@dataclass
class HandoffStep:
    agent_id: str
    agent_name: str
    emoji: str
    input_summary: str
    output_summary: str
    confidence: float
    duration_ms: float
    status: str = "success"


@dataclass
class SwarmResult:
    insight: str
    key_finding: str
    confidence: float
    severity: str          # CRITICAL | HIGH | MEDIUM | LOW
    evidence: List[str]
    actions: List[str]
    agent_chain: List[HandoffStep]
    raw_thoughts: List[str]
    total_duration_ms: float
    agent_used: str = "SwarmOrchestrator"
    priority: str = "THIS_WEEK"


def _safe_parse_json(text: str) -> dict:
    """Safely extract and parse the first JSON object from a string."""
    try:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return {}


class SwarmOrchestrator:
    """
    Orchestrates a 3-agent reasoning chain:
      Step 1 — CriticAgent:        Analyses the query, finds risks & evidence
      Step 2 — ConsensusAgent:     Synthesizes critique into specific insight
      Step 3 — ActionPlaybook:     Generates concrete, executable action items

    Each step receives the previous agent's structured JSON output as context.
    """

    def __init__(self, system_prompt: Optional[str] = None):
        self.system_prompt = system_prompt or (
            "You are a multi-agent cognitive reasoning system built on Google Antigravity. "
            "You reason in structured, specific, evidence-based steps."
        )

    async def run(self, query: str, doc_context: str = "") -> SwarmResult:
        start_total = time.time()
        chain: List[HandoffStep] = []
        all_thoughts: List[str] = []
        antigravity = get_antigravity_client()

        # ── AGENT 1: CRITIC ───────────────────────────────────────────────
        t0 = time.time()
        logger.info("[SwarmOrchestrator] Step 1: CriticAgent dispatched")

        critic_prompt = f"""{self.system_prompt}

ROLE: You are the Critic Agent. Your only job is to rigorously analyse the query below.
You must be SPECIFIC — not generic. Instead of "sales are down" say "Sales in sector G-13 down 25% since Q3 due to competitor expansion".

Return ONLY valid JSON:
{{
  "critique": "<2-3 sentence specific analysis>",
  "risks": ["<specific risk 1>", "<specific risk 2>"],
  "confidence": <0.0-1.0>,
  "severity": "<CRITICAL|HIGH|MEDIUM|LOW>",
  "evidence": ["<specific fact 1>", "<specific fact 2>", "<specific fact 3>"]
}}

QUERY: {query}
{chr(10) + "DOCUMENT CONTEXT:" + chr(10) + doc_context if doc_context else ""}"""

        critic_raw = await antigravity.generate(critic_prompt)
        critic_text = ""
        if hasattr(critic_raw, 'data') and isinstance(critic_raw.data, dict):
            critic_text = critic_raw.data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            critic_text = str(critic_raw)
            
        critic_data = _safe_parse_json(critic_text) or {
            "critique": critic_text[:300] or "Critical analysis performed.",
            "risks": ["Unverified assumptions in the query"],
            "confidence": 0.72,
            "severity": "MEDIUM",
            "evidence": ["Analysis derived from query context"]
        }

        all_thoughts.append(f"[Critic] {critic_data.get('critique', '')[:180]}")
        chain.append(HandoffStep(
            agent_id="critic",
            agent_name="Critic Agent",
            emoji="🔍",
            input_summary=query[:100],
            output_summary=critic_data.get("critique", "")[:120],
            confidence=float(critic_data.get("confidence", 0.72)),
            duration_ms=(time.time() - t0) * 1000,
        ))

        # ── AGENT 2: CONSENSUS ────────────────────────────────────────────
        t1 = time.time()
        logger.info("[SwarmOrchestrator] Step 2: ConsensusAgent dispatched")

        consensus_prompt = f"""{self.system_prompt}

ROLE: You are the Consensus Agent. You receive the Critic's analysis and synthesize it into ONE clear, specific, actionable insight.
Specificity is mandatory — use numbers, locations, timeframes where possible.

CRITIC'S ANALYSIS:
{json.dumps(critic_data, indent=2)}

ORIGINAL QUERY: {query}

Return ONLY valid JSON:
{{
  "key_finding": "<One-line headline — specific, not generic>",
  "insight": "<2-4 sentence detailed insight with specifics>",
  "confidence": <0.0-1.0>,
  "severity": "<CRITICAL|HIGH|MEDIUM|LOW>",
  "evidence": ["<specific evidence 1>", "<specific evidence 2>", "<specific evidence 3>"]
}}"""

        consensus_raw = await antigravity.generate(consensus_prompt)
        consensus_text = ""
        if hasattr(consensus_raw, 'data') and isinstance(consensus_raw.data, dict):
            consensus_text = consensus_raw.data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            consensus_text = str(consensus_raw)
            
        consensus_data = _safe_parse_json(consensus_text) or {
            "key_finding": "Synthesis of critical analysis complete",
            "insight": critic_data.get("critique", consensus_text[:300]),
            "confidence": critic_data.get("confidence", 0.75),
            "severity": critic_data.get("severity", "MEDIUM"),
            "evidence": critic_data.get("evidence", [])
        }

        all_thoughts.append(f"[Consensus] {consensus_data.get('key_finding', '')}: {consensus_data.get('insight', '')[:160]}")
        chain.append(HandoffStep(
            agent_id="consensus",
            agent_name="Consensus Agent",
            emoji="🤝",
            input_summary=f"Critic: {critic_data.get('critique', '')[:80]}",
            output_summary=consensus_data.get("key_finding", "")[:120],
            confidence=float(consensus_data.get("confidence", 0.8)),
            duration_ms=(time.time() - t1) * 1000,
        ))

        # ── AGENT 3: ACTION PLAYBOOK ──────────────────────────────────────
        t2 = time.time()
        logger.info("[SwarmOrchestrator] Step 3: ActionPlaybookAgent dispatched")

        playbook_prompt = f"""{self.system_prompt}

ROLE: You are the Action Playbook Agent. You generate 3-5 CONCRETE, EXECUTABLE actions based on the consensus insight.
Each action must have: What to do + Who owns it + When to do it.

CONSENSUS INSIGHT: {consensus_data.get('insight', '')}
SEVERITY: {consensus_data.get('severity', 'MEDIUM')}
EVIDENCE: {consensus_data.get('evidence', [])}

Return ONLY valid JSON:
{{
  "actions": [
    "<Action 1: specific task — owner — deadline>",
    "<Action 2: specific task — owner — deadline>",
    "<Action 3: specific task — owner — deadline>"
  ],
  "priority": "<IMMEDIATE|THIS_WEEK|THIS_MONTH>",
  "expected_outcome": "<What measurable success looks like>"
}}"""

        playbook_raw = await antigravity.generate(playbook_prompt)
        playbook_text = ""
        if hasattr(playbook_raw, 'data') and isinstance(playbook_raw.data, dict):
            playbook_text = playbook_raw.data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            playbook_text = str(playbook_raw)
            
        playbook_data = _safe_parse_json(playbook_text) or {
            "actions": [
                "Validate the identified risk with domain expert — Lead Analyst — 48h",
                "Gather supporting data to strengthen evidence base — Data Team — 72h",
                "Present severity report to decision maker — Project Lead — This week"
            ],
            "priority": "THIS_WEEK",
            "expected_outcome": "Clear accountability with evidence-backed decision"
        }

        all_thoughts.append(
            f"[Playbook] Priority={playbook_data.get('priority','?')}: "
            + " | ".join(playbook_data.get("actions", [])[:2])
        )
        chain.append(HandoffStep(
            agent_id="action_playbook",
            agent_name="Action Playbook",
            emoji="📋",
            input_summary=consensus_data.get("key_finding", "")[:80],
            output_summary=f"{len(playbook_data.get('actions', []))} actions — {playbook_data.get('priority', 'THIS_WEEK')}",
            confidence=float(consensus_data.get("confidence", 0.8)),
            duration_ms=(time.time() - t2) * 1000,
        ))

        # Submit Swarm Trace back to Antigravity
        try:
            swarm_trace_data = {
                "session_type": "swarm_orchestrator",
                "query": query,
                "confidence": float(consensus_data.get("confidence", 0.75)),
                "severity": consensus_data.get("severity", "MEDIUM"),
                "total_duration_ms": (time.time() - start_total) * 1000,
                "chain": [
                    {
                        "agent_id": step.agent_id,
                        "agent_name": step.agent_name,
                        "input": step.input_summary,
                        "output": step.output_summary,
                        "confidence": step.confidence,
                        "duration_ms": step.duration_ms
                    }
                    for step in chain
                ]
            }
            await antigravity._post("/traces/submit", swarm_trace_data)
        except Exception as trace_err:
            logger.warning(f"Failed to submit swarm trace to Antigravity: {trace_err}")

        return SwarmResult(
            insight=consensus_data.get("insight", all_thoughts[1] if len(all_thoughts) > 1 else "Analysis complete."),
            key_finding=consensus_data.get("key_finding", "Swarm analysis complete"),
            confidence=float(consensus_data.get("confidence", 0.75)),
            severity=consensus_data.get("severity", critic_data.get("severity", "MEDIUM")),
            evidence=consensus_data.get("evidence", critic_data.get("evidence", [])),
            actions=playbook_data.get("actions", []),
            agent_chain=chain,
            raw_thoughts=all_thoughts,
            total_duration_ms=(time.time() - start_total) * 1000,
            priority=playbook_data.get("priority", "THIS_WEEK"),
        )
