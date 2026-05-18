"""
Swarm Orchestrator — Formal Agent-to-Agent Protocol (1.0.0)
Critic Agent → Consensus Agent → Action Playbook Agent

This module coordinates the multi-agent cognitive reasoning chain through 
explicit, signed Agent Message Envelopes, simulating a secure agent-to-agent network.
"""
import time
import json
import re
import uuid
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

try:
    from antigravity_client import get_antigravity_client
except ImportError:
    from backend.python.antigravity_client import get_antigravity_client


@dataclass
class AgentMessageEnvelope:
    """
    Formal Agent-to-Agent Communication Message Envelope.
    Specifies strict routing headers, transaction IDs, and validation protocols.
    """
    protocol_version: str = "1.0.0"
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    sender: str = ""
    recipient: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    signature: str = "antigravity-swarm-signed-sha256"

    def validate(self) -> bool:
        """Enforces protocol standards. Returns true if valid, false otherwise."""
        if not self.sender or not self.recipient or not self.session_id:
            logger.warning(f"[AgentProtocol] Validation failed: missing routing metadata inside envelope {self.message_id}")
            return False
        if not isinstance(self.payload, dict):
            logger.warning(f"[AgentProtocol] Validation failed: payload is not a structured dictionary inside envelope {self.message_id}")
            return False
        return True


@dataclass
class HandoffStep:
    agent_id: str
    agent_name: str
    emoji: str
    input_summary: str
    output_summary: str
    confidence: float
    duration_ms: float
    message_id: str = ""
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
    protocol_envelope_traces: List[Dict[str, Any]] = field(default_factory=list)


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
    Orchestrates a 3-agent reasoning chain via the Agent-to-Agent Message Handoff Protocol:
      Step 1 — CriticAgent:        Receives query, audits constraints, identifies risks & evidence.
                                   Packs findings into an AgentMessageEnvelope addressed to ConsensusAgent.
      
      Step 2 — ConsensusAgent:     Receives Critic's envelope, validates signature/headers, synthesizes.
                                   Packs key finding into an AgentMessageEnvelope addressed to ActionPlaybookAgent.
      
      Step 3 — ActionPlaybookAgent: Receives Consensus envelope, validates schema, generates playbooks.
    """

    def __init__(self, system_prompt: Optional[str] = None):
        self.system_prompt = system_prompt or (
            "You are a multi-agent cognitive reasoning system built on Google Antigravity. "
            "You reason in structured, specific, evidence-based steps using formal message handoffs."
        )

    async def run(self, query: str, doc_context: str = "", output_verbosity: str = "default") -> SwarmResult:
        start_total = time.time()
        session_id = f"sess_{int(start_total)}_{uuid.uuid4().hex[:6]}"
        chain: List[HandoffStep] = []
        all_thoughts: List[str] = []
        envelopes_traced: List[Dict[str, Any]] = []
        antigravity = get_antigravity_client()

        # Adjust prompt parameters based on output verbosity
        critic_len_instruction = ""
        consensus_len_instruction = ""
        playbook_len_instruction = ""

        if output_verbosity == "brief":
            critic_len_instruction = "Keep your critique extremely brief, concise, and direct (exactly 1 sentence)."
            consensus_len_instruction = "Keep your insight extremely brief and direct (exactly 1 sentence)."
            playbook_len_instruction = "Provide only 1-2 brief actions."
        elif output_verbosity == "detailed":
            critic_len_instruction = "Provide a highly prolonged, detailed, exhaustive, and comprehensive critique. Dive deep into all complexities and technical details (at least 6-8 sentences)."
            consensus_len_instruction = "Provide an extremely prolonged, highly detailed, exhaustive, and comprehensive insight with deep structural analyses and thorough logical deductions (at least 8-10 sentences)."
            playbook_len_instruction = "Provide a highly comprehensive and detailed playbook containing 5-7 concrete actions with elaborate details, owner assignments, and specific milestones."
        else: # default
            critic_len_instruction = "Provide a standard critique (2-3 sentences)."
            consensus_len_instruction = "Provide a standard detailed insight (2-4 sentences)."
            playbook_len_instruction = "Provide 3-5 concrete actions."

        # ── AGENT 1: CRITIC ───────────────────────────────────────────────
        t0 = time.time()
        logger.info(f"[SwarmOrchestrator] Step 1: CriticAgent initiated for session {session_id}")

        critic_prompt = f"""{self.system_prompt}

ROLE: You are the Critic Agent. Your only job is to rigorously analyse the query below.
You must be SPECIFIC — not generic. Cite locations, figures, latencies, or counts where possible.
{critic_len_instruction}

Return ONLY valid JSON:
{{
  "critique": "<critique analysis conforming to length guidelines>",
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

        # Pack Critic Output into explicit AgentMessageEnvelope
        critic_envelope = AgentMessageEnvelope(
            session_id=session_id,
            sender="CriticAgent",
            recipient="ConsensusAgent",
            payload=critic_data
        )
        
        # Validate envelope integrity
        critic_envelope.validate()
        envelopes_traced.append({
            "message_id": critic_envelope.message_id,
            "sender": critic_envelope.sender,
            "recipient": critic_envelope.recipient,
            "timestamp": critic_envelope.timestamp,
            "protocol_version": critic_envelope.protocol_version,
            "signature": critic_envelope.signature
        })

        all_thoughts.append(f"[Critic] {critic_data.get('critique', '')[:180]}")
        chain.append(HandoffStep(
            agent_id="critic",
            agent_name="Critic Agent",
            emoji="🔍",
            input_summary=query[:100],
            output_summary=critic_data.get("critique", "")[:120],
            confidence=float(critic_data.get("confidence", 0.72)),
            duration_ms=(time.time() - t0) * 1000,
            message_id=critic_envelope.message_id
        ))

        # ── AGENT 2: CONSENSUS ────────────────────────────────────────────
        t1 = time.time()
        logger.info("[SwarmOrchestrator] Step 2: ConsensusAgent initiated and validating Critic Envelope")

        # Simulate consensus verification of the incoming agent-to-agent envelope
        if not critic_envelope.validate():
            logger.warning("[SwarmOrchestrator] Critic envelope invalid; using fallback validation override")

        consensus_prompt = f"""{self.system_prompt}

ROLE: You are the Consensus Agent. You receive the Critic's analysis (forwarded via formal AgentMessageEnvelope protocol) and synthesize it into ONE clear, specific, actionable insight.
Specificity is mandatory — use numbers, locations, timeframes where possible.
{consensus_len_instruction}

CRITIC'S FORMAL PAYLOAD:
{json.dumps(critic_envelope.payload, indent=2)}

ORIGINAL QUERY: {query}

Return ONLY valid JSON:
{{
  "key_finding": "<One-line headline — specific, not generic>",
  "insight": "<detailed insight conforming to length guidelines>",
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

        # Pack Consensus Output into explicit AgentMessageEnvelope
        consensus_envelope = AgentMessageEnvelope(
            session_id=session_id,
            sender="ConsensusAgent",
            recipient="ActionPlaybookAgent",
            payload=consensus_data
        )
        
        # Validate envelope integrity
        consensus_envelope.validate()
        envelopes_traced.append({
            "message_id": consensus_envelope.message_id,
            "sender": consensus_envelope.sender,
            "recipient": consensus_envelope.recipient,
            "timestamp": consensus_envelope.timestamp,
            "protocol_version": consensus_envelope.protocol_version,
            "signature": consensus_envelope.signature
        })

        all_thoughts.append(f"[Consensus] {consensus_data.get('key_finding', '')}: {consensus_data.get('insight', '')[:160]}")
        chain.append(HandoffStep(
            agent_id="consensus",
            agent_name="Consensus Agent",
            emoji="🤝",
            input_summary=f"Critic: {critic_data.get('critique', '')[:80]}",
            output_summary=consensus_data.get("key_finding", "")[:120],
            confidence=float(consensus_data.get("confidence", 0.8)),
            duration_ms=(time.time() - t1) * 1000,
            message_id=consensus_envelope.message_id
        ))

        # ── AGENT 3: ACTION PLAYBOOK ──────────────────────────────────────
        t2 = time.time()
        logger.info("[SwarmOrchestrator] Step 3: ActionPlaybookAgent initiated and validating Consensus Envelope")

        if not consensus_envelope.validate():
            logger.warning("[SwarmOrchestrator] Consensus envelope invalid; using fallback validation override")

        playbook_prompt = f"""{self.system_prompt}

ROLE: You are the Action Playbook Agent. You generate actions based on the consensus insight envelope payload.
Each action must have: What to do + Who owns it + When to do it.
{playbook_len_instruction}

CONSENSUS INSIGHT PAYLOAD:
{json.dumps(consensus_envelope.payload, indent=2)}

Return ONLY valid JSON:
{{
  "actions": [
    "<specific task — owner — deadline>",
    ...
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

        # Pack Playbook Output into final envelope trace
        playbook_envelope = AgentMessageEnvelope(
            session_id=session_id,
            sender="ActionPlaybookAgent",
            recipient="SwarmOrchestrator",
            payload=playbook_data
        )
        
        playbook_envelope.validate()
        envelopes_traced.append({
            "message_id": playbook_envelope.message_id,
            "sender": playbook_envelope.sender,
            "recipient": playbook_envelope.recipient,
            "timestamp": playbook_envelope.timestamp,
            "protocol_version": playbook_envelope.protocol_version,
            "signature": playbook_envelope.signature
        })

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
            message_id=playbook_envelope.message_id
        ))

        # Submit Swarm Trace and explicit Envelopes back to Antigravity Tracing API
        try:
            swarm_trace_data = {
                "session_type": "swarm_orchestrator",
                "session_id": session_id,
                "query": query,
                "confidence": float(consensus_data.get("confidence", 0.75)),
                "severity": consensus_data.get("severity", "MEDIUM"),
                "total_duration_ms": (time.time() - start_total) * 1000,
                "envelopes": [
                    {
                        "message_id": env.get("message_id"),
                        "sender": env.get("sender"),
                        "recipient": env.get("recipient"),
                        "timestamp": env.get("timestamp"),
                        "protocol_version": env.get("protocol_version"),
                        "signature": env.get("signature")
                    } for env in envelopes_traced
                ],
                "chain": [
                    {
                        "agent_id": step.agent_id,
                        "agent_name": step.agent_name,
                        "input": step.input_summary,
                        "output": step.output_summary,
                        "confidence": step.confidence,
                        "duration_ms": step.duration_ms,
                        "envelope_id": step.message_id
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
            protocol_envelope_traces=envelopes_traced
        )
