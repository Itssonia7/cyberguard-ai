import socket

def grab_banner(target: str, port: int) -> str:
    """
    Connects to a specific target and port via a TCP socket to retrieve 
    the service's welcome banner. Useful for software version fingerprinting.
    """
    print(f"[*] Tool execution: Grabbing banner on {target}:{port}...")
    try:
        # Create a standard TCP socket
        # socket.AF_INET specifies IPv4, socket.SOCK_STREAM specifies TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a tight timeout so the agent doesn't hang indefinitely on silent ports
            s.settimeout(3.0)
            s.connect((target, port))
            
            # Send a generic newline to prompt a response payload (common for HTTP/SSH/FTP)
            s.sendall(b"HEAD / HTTP/1.1\r\n\r\n\n")
            
            # Receive up to 1024 bytes of the banner text
            banner = s.recv(1024)
            return banner.decode('utf-8', errors='ignore').strip()
            
    except socket.timeout:
        return f"Error: Connection timed out on port {port}."
    except Exception as e:
        return f"Error executing banner grab on port {port}: {str(e)}"