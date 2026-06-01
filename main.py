import sys
import uuid
from datetime import datetime
from config import settings
from models import SessionState, AgentAction
from memory import SessionMemoryManager
from scanner import NetworkScanner
from agent import CyberGuardAgent

# Import the actual security tool functions we built
from tools.banner_grab import grab_banner
from tools.cve_lookup import lookup_cve
from tools.exploit_suggest import suggest_exploit

def run_autonomous_assessment(target: str, max_turns: int = 5):
    """
    Orchestrates the entire end-to-end lifecycle of CyberGuard AI.
    Runs the initial network scan, binds tools to the Gemini reasoning engine,
    tracks state execution loops, and outputs the final markdown audit report.
    """
    # 1. Establish unique tracking signatures
    session_id = f"cg-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    print(f"[+] Initializing CyberGuard AI Autonomous Session: {session_id}")
    print(f"[*] Target Asset Scoped: {target}")
    print("-" * 60)

    # 2. Instantiate foundational layers
    memory_mgr = SessionMemoryManager(session_id=session_id, target=target)
    session_state = memory_mgr.load_session()
    
    # 3. Step 1: Execute the initial sensory network discovery scan
    scanner = NetworkScanner(target=target)
    scan_results = scanner.run_port_scan(ports="21,22,80,443,8080")
    
    # Save discovery results straight to state
    session_state.discovered_host_info = scan_results
    memory_mgr.save_session(session_state)
    
    if scan_results.status == "down" or not scan_results.open_ports:
        print("[!] Target appears down or no common open ports discovered. Concluding assessment early.")
        from reporter import SecurityReporter
        reporter = SecurityReporter(session_state)
        reporter.generate_markdown_report()
        return

    # 4. Step 2: Initialize Brain Engine and link real functional execution tools
    agent = CyberGuardAgent(target=target)
    
    # Registering tools matching the core keywords the LLM expects
    agent.register_tool("grab_banner", grab_banner)
    agent.register_tool("lookup_cve", lookup_cve)
    agent.register_tool("suggest_exploit", suggest_exploit)

    print(f"[+] Operational tools linked to Gemini Brain: {list(agent.tool_registry.keys())}")
    print("-" * 60)

    # 5. Core Autonomous Step Loop
    turn = 0
    while turn < max_turns:
        turn += 1
        print(f"\n[*] --- Starting Autonomous Turn {turn} of {max_turns} ---")
        
        # Run a reasoning step (Contact Gemini)
        proposed_action = agent.run_reasoning_step(session_state)
        
        # If Gemini returned no function calls, it has finished analyzing or hit a natural stop
        if not proposed_action:
            print("[+] Brain indicated analysis completeness. Exiting reasoning loop.")
            break
            
        tool_name = proposed_action.tool_name
        tool_args = proposed_action.arguments
        
        # Guard rail: Make sure the chosen tool actually exists in our dictionary registry
        if tool_name in agent.tool_registry:
            try:
                # Dynamically retrieve and run the tool function passing arguments securely
                # Filter arguments to dynamically prevent unexpected parameters blowing up the tool
                execution_func = agent.tool_registry[tool_name]
                
                # Execute the real python tool function
                if tool_name == "grab_banner":
                    # Fall back to standard defaults if LLM drops required keys
                    p = int(tool_args.get("port", 22))
                    raw_result = execution_func(target=target, port=p)
                elif tool_name == "lookup_cve":
                    cve = str(tool_args.get("cve_id", ""))
                    raw_result = execution_func(cve_id=cve)
                elif tool_name == "suggest_exploit":
                    summary = str(tool_args.get("service_summary", "Generic network endpoint"))
                    raw_result = execution_func(service_summary=summary)
                else:
                    raw_result = "Tool format configuration mismatched."

                # Update the action record with the real output findings
                proposed_action.result_summary = raw_result
                print(f"[+] Tool executed successfully. Summary gathered.")

                # If a banner was grabbed, inject a helpful high-level note to the structural findings summary
                if tool_name == "grab_banner" and "Error" not in raw_result:
                    session_state.findings_summary.append(f"Successfully grabbed banner on port {tool_args.get('port')}: {raw_result}")

            except Exception as e:
                proposed_action.result_summary = f"Execution error running tool handler: {str(e)}"
                print(f"[!] Tool execution crash: {e}")
        else:
            proposed_action.result_summary = f"Error: Tool '{tool_name}' is not registered within this agent's chassis."
            print(f"[!] Brain attempted to access unregistered tool: {tool_name}")

        # Record this action turn permanently to memory state so Gemini sees it on next loop iteration
        session_state.actions_taken.append(proposed_action)
        memory_mgr.save_session(session_state)
        
        # Small defensive separator
        print("-" * 40)

    # 6. Step 3: Assessment complete! Compile the final executive report artifact
    print("\n" + "="*60)
    print("[+] Autonomous cycle concluded. Triggering document serialization...")
    from reporter import SecurityReporter
    reporter = SecurityReporter(session_state)
    final_report_path = reporter.generate_markdown_report()
    print(f"[+] Process complete. Final Report Asset: {final_report_path}")
    print("="*60)

if __name__ == "__main__":
    # Target fallback logic: use user args if passed, else fallback safely to localhost configuration
    target_to_test = sys.argv[1] if len(sys.argv) > 1 else settings.DEFAULT_TARGET
    
    print("[*] CyberGuard AI Shell Active.")
    run_autonomous_assessment(target=target_to_test)