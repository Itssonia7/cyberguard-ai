# test_scanner.py
from scanner import NetworkScanner

def test_scanner_module():
    print("[*] Initializing NetworkScanner test against localhost...")
    
    # We target 127.0.0.1 for local, completely safe verification
    scanner = NetworkScanner(target="127.0.0.1")
    
    try:
        # Run a scan against common ports
        results = scanner.run_port_scan(ports="22,80,443")
        
        print("\n[+] Scan Execution Complete!")
        print(f"    Target Analyzed: {results.target}")
        print(f"    Host Status:     {results.status}")
        print(f"    Discovered Open Ports Count: {len(results.open_ports)}")
        
        for p in results.open_ports:
            print(f"     -> Port Found: {p.port}/{p.protocol} | State: {p.state} | Service: {p.service}")
            
    except Exception as e:
        print(f"[!] Test failed with error: {e}")

if __name__ == "__main__":
    test_scanner_module()