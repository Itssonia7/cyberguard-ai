from config import settings
from models import PortScanResult, HostScanResult

def verify_setup():
    print("[*] Verifying folder initialization and configuration loading...")
    print(f"    Target Model Set: {settings.GEMINI_MODEL}")
    
    # Try validating data through the schema
    test_port = PortScanResult(port=22, state="open", service="ssh", version="OpenSSH 8.9p1")
    test_host = HostScanResult(target=settings.DEFAULT_TARGET, status="up", open_ports=[test_port])
    
    print(f"    Pydantic Schema Check: Successfully parsed target {test_host.target} with service {test_host.open_ports[0].service}")
    print("[+] Scratch environment verification complete. Ready for development!")

if __name__ == "__main__":
    verify_setup()