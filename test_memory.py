# test_memory.py
from memory import SessionMemoryManager
from models import AgentAction

def test_memory_serialization():
    print("[*] Simulating agent loop state persistence...")
    
    # Initialize the memory manager
    memory_mgr = SessionMemoryManager(session_id="test-1337", target="127.0.0.1")
    
    # Load state (should create a brand new one)
    active_state = memory_mgr.load_session()
    
    # Simulate the agent recording an action taken
    mock_action = AgentAction(
        tool_name="banner_grab",
        arguments={"port": 22, "target": "127.0.0.1"},
        result_summary="SSH-2.0-OpenSSH_9.6p1 Ubuntu"
    )
    active_state.actions_taken.append(mock_action)
    active_state.findings_summary.append("Discovered active SSH daemon version.")
    
    # Persist it to disk
    print("[*] Saving updated session state to JSON...")
    memory_mgr.save_session(active_state)
    
    # Read it back to verify data integrity
    print("[*] Reading session data back from disk to verify integrity...")
    reloaded_state = memory_mgr.load_session()
    
    assert len(reloaded_state.actions_taken) == 1
    assert reloaded_state.actions_taken[0].tool_name == "banner_grab"
    
    print(f"\n[+] Success! Memory persisted perfectly to: {memory_mgr.filepath}")
    print(f"    Recovered Action: {reloaded_state.actions_taken[0].tool_name}")
    print(f"    Recovered Summary: {reloaded_state.findings_summary[0]}")

if __name__ == "__main__":
    test_memory_serialization()