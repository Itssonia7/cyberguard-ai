import subprocess
import re
from datetime import datetime
from typing import Optional
from models import HostScanResult, PortScanResult

class NetworkScanner:
    """
    A secure wrapper around the system's nmap binary.
    Executes scans and parses raw textual output into structured Pydantic models.
    """

    def __init__(self, target: str):
        self.target = target

    def _is_valid_target(self, target: str) -> bool:
        """
        A strict security check to ensure targets are structural strings.
        Prevents dangerous shell injection attacks by ensuring the target
        looks like a valid domain or IP address before passing it to a subprocess.
        """
        # Basic check: allow only alphanumeric characters, dots, dashes, and colons
        # Disallows characters like ;, &, |, $, etc., used in shell chaining.
        return bool(re.match(r"^[a-zA-Z0-9\.\-\:]+$", target))

    def run_port_scan(self, ports: str = "21,22,80,443,8080") -> HostScanResult:
        """
        Executes a basic Nmap TCP scan against the specified ports.
        Maps the unstructured CLI output into a clean HostScanResult object.
        """
        if not self._is_valid_target(self.target):
            raise ValueError(f"[!] Security Alert: Malicious or invalid target format detected: '{self.target}'")

        print(f"[*] Initiating discovery scan against {self.target} on ports: {ports}...")

        # Constructing the nmap arguments list securely without using shell=True
        # -sV tries to look up service version strings if possible
        # -F is not used here; we explicitly specify the target ports passed by the agent
        cmd = ["nmap", "-p", ports, self.target]

        try:
            # Execute command safely; capture stdout and stderr as text strings
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return self._parse_nmap_output(result.stdout)
            
        except FileNotFoundError:
            print("[!] Error: 'nmap' binary not found on this system.")
            print("[!] Please install it using: sudo apt update && sudo apt install nmap")
            # Return an empty/down status structure so the agent loop doesn't crash completely
            return HostScanResult(target=self.target, status="down")
        except subprocess.CalledProcessError as e:
            print(f"[!] Nmap execution encountered an unexpected error: {e.stderr}")
            return HostScanResult(target=self.target, status="down")

    def _parse_nmap_output(self, raw_stdout: str) -> HostScanResult:
        """
        Parses raw text output from Nmap using Regular Expressions.
        Extracts open ports, service profiles, and operational state.
        """
        open_ports_list = []
        host_status = "down"

        # Regex patterns to parse standard Nmap format lines
        # Example line: "Host is up (0.00017s latency)."
        host_up_pattern = re.compile(r"Host is up")
        
        # Example line: "22/tcp open  ssh     OpenSSH 8.9p1"
        # Matches: group(1)=port, group(2)=protocol, group(3)=state, group(4)=service
        port_pattern = re.compile(r"(\d+)/(\w+)\s+(open|filtered|closed)\s+(\S+)")

        for line in raw_stdout.splitlines():
            # 1. Determine if the host is up
            if host_up_pattern.search(line):
                host_status = "up"
                continue

            # 2. Check for port status signatures
            match = port_pattern.search(line)
            if match:
                port_num = int(match.group(1))
                protocol_type = match.group(2)
                port_state = match.group(3)
                service_name = match.group(4)

                # We primarily prioritize capturing active risk vectors ('open' ports)
                if port_state == "open":
                    port_obj = PortScanResult(
                        port=port_num,
                        protocol=protocol_type,
                        state=port_state,
                        service=service_name,
                        version=None # Can be augmented later by banner grabbing tools
                    )
                    open_ports_list.append(port_obj)

        return HostScanResult(
            target=self.target,
            status=host_status,
            open_ports=open_ports_list,
            scan_time=datetime.utcnow()
        )