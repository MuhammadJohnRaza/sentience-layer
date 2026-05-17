import asyncio
import os
import sys
import time

# Force UTF-8 output so Unicode characters don't crash Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Ensure backend/python is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'python'))

from dotenv import load_dotenv
load_dotenv()

from backend.python.agents import (
    ActionCategoryAgent,
    ActionPlaybookAgent,
    ActionPriorityAgent,
    ActionRankingAgent,
    AdversarialTestAgent,
    CausalInferenceAgent,
    ConsensusAgent,
    CriticAgent,
    DebateAgent,
    DeterministicAgent,
    DreamAgent,
    EconomicAgent,
    EthicsAgent,
    MemoryEnabledAgent,
    OpportunityAnalystAgent,
    PersonalizationAgent,
    PremonitionAgent,
    UncertaintyAgent
)

AGENT_CLASSES = {
    "ActionCategoryAgent": ActionCategoryAgent,
    "ActionPlaybookAgent": ActionPlaybookAgent,
    "ActionPriorityAgent": ActionPriorityAgent,
    "ActionRankingAgent": ActionRankingAgent,
    "AdversarialTestAgent": AdversarialTestAgent,
    "CausalInferenceAgent": CausalInferenceAgent,
    "ConsensusAgent": ConsensusAgent,
    "CriticAgent": CriticAgent,
    "DebateAgent": DebateAgent,
    "DeterministicAgent": DeterministicAgent,
    "DreamAgent": DreamAgent,
    "EconomicAgent": EconomicAgent,
    "EthicsAgent": EthicsAgent,
    "MemoryEnabledAgent": MemoryEnabledAgent,
    "OpportunityAnalystAgent": OpportunityAnalystAgent,
    "PersonalizationAgent": PersonalizationAgent,
    "PremonitionAgent": PremonitionAgent,
    "UncertaintyAgent": UncertaintyAgent
}

async def test_agent(name, agent_class):
    print(f"\n--- Testing Agent: {name} ---")
    start_time = time.time()
    try:
        # Instantiate agent
        agent = agent_class(config={})
        
        # Test ReAct reasoning loop (run just 1 step to be quick and clean)
        agent.max_reasoning_steps = 1
        
        print(f"[{name}] Running reasoning loop...")
        result = await agent.reason_and_act("Verify the cognitive system is operational.")
        
        latency = (time.time() - start_time) * 1000
        if result.success:
            print(f"[SUCCESS] {name} initialized and reasoned successfully in {latency:.2f}ms!")
            # Print a snippet of the thought if available
            if result.reasoning_chain:
                thought_text = result.reasoning_chain[0].thought or ""
                # Sanitize: replace un-encodable chars with '?'
                safe_thought = thought_text.encode('ascii', errors='replace').decode('ascii')
                print(f"Thought: {safe_thought[:120]}")
            return True, None
        else:
            print(f"[FAILED] {name} reason_and_act returned failure: {result.error}")
            return False, result.error
            
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        print(f"[ERROR] {name} threw exception after {latency:.2f}ms: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

async def main():
    print("======================================================================")
    print("                     SENTIENCE COGNITIVE AGENTS TESTER                ")
    print("======================================================================")
    
    results = {}
    
    for name, agent_class in AGENT_CLASSES.items():
        success, err = await test_agent(name, agent_class)
        results[name] = {"success": success, "error": err}
        
    print("\n======================================================================")
    print("                           SUMMARY REPORT                             ")
    print("======================================================================")
    
    passed_count = 0
    failed_count = 0
    
    for name, res in results.items():
        if res["success"]:
            print(f" [PASS] {name:<30} Status: Functional")
            passed_count += 1
        else:
            print(f" [FAIL] {name:<30} Status: Error - {res['error']}")
            failed_count += 1
            
    print("----------------------------------------------------------------------")
    print(f"Total Agents Tested: {len(results)}")
    print(f"Passed: {passed_count} / {len(results)}")
    print(f"Failed: {failed_count} / {len(results)}")
    print("======================================================================")
    
    # Close any global Antigravity client sessions to exit cleanly
    from backend.python.antigravity_client import get_antigravity_client
    client = get_antigravity_client()
    await client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
