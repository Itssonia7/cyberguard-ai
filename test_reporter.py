# test_reporter.py
from models import SessionState, HostScanResult, PortScanResult, AgentAction
from reporter import SecurityReporter

def test_reporting_suite():
    print("[*] Generating mock asset state context...")
    
    # 1. Simulate an advanced scan state
    mock_port = PortScanResult(port=22, state="open", service="ssh")
    mock_host = HostScanResult(target="127.0.0.1", status="up", open_ports=[mock_port])
    
    state = SessionState(
        session_id="audit-99",
        target="127.0.0.1",
        discovered_host_info=mock_host,
        findings_summary=["Target host exposes an open SSH configuration management vector."]
    )
    
    # 2. Simulate tool output record
    state.actions_taken.append(AgentAction(
        tool_name="grab_banner",
        arguments={"port": 22},
        result_summary="SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.16"
    ))
    
    # 3. Fire compiler engine
    reporter = SecurityReporter(session_state=state)
    output_file = reporter.generate_markdown_report()
    
    # Check if report actually exists
    assert output_file.exists()
    print(f"[+] Success! Check your `{output_file}` file to view the generated document.")

if __name__ == "__main__":
    test_reporting_suite()