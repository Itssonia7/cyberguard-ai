# test_agent.py
import os
from agent import CyberGuardAgent
from models import SessionState, HostScanResult, PortScanResult

from dotenv import load_dotenv
# Explicitly load the .env file from the current directory
load_dotenv()

# Mock tool functions that match our schema expectations
def mock_banner_grab(target: str, port: int):
    """Connects to a port via sockets to capture its service banner."""
    return f"Simulated banner for {target}:{port} -> OpenSSH 8.9p1"

def test_agent_brain():
    print("[*] Testing CyberGuard Agent Brain Setup...")
    
    # Simple check: make sure user has updated their API key or configured environment
    if "AIzaSy" in os.environ.get("GEMINI_API_KEY", "AIzaSyYourKeyGoesHere"):
        print("[!] Warning: You are using a placeholder API key. Ensure a real key is active in your environment.")

    # 1. Instantiate our Agent
    agent = CyberGuardAgent(target="127.0.0.1")
    
    # 2. Register our dummy tool into the agent's brain registry
    agent.register_tool("mock_banner_grab", mock_banner_grab)
    
    # 3. Simulate a session state where port 22 was found open
    mock_port = PortScanResult(port=22, state="open", service="ssh")
    mock_scan = HostScanResult(target="127.0.0.1", status="up", open_ports=[mock_port])
    
    session = SessionState(
        session_id="test-session-1337",
        target="127.0.0.1",
        discovered_host_info=mock_scan
    )
    
    print("[*] Session state prepared. Simulating one reasoning step...")
    decision = agent.run_reasoning_step(session)
    
    if decision:
        print(f"\n[+] Success! Agent selected tool: {decision.tool_name}")
        print(f"    Arguments targeted: {decision.arguments}")
    else:
        print("\n[-] Agent reviewed data but did not trigger a specific function call.")

if __name__ == "__main__":
    test_agent_brain()