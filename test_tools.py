# test_tools.py
from tools.banner_grab import grab_banner
from tools.cve_lookup import lookup_cve

def verify_standalone_tools():
    print("[*] Verification 1: Running local Banner Grab against localhost port 22...")
    # This checks if your local SSH port responds with its banner string
    banner_result = grab_banner("127.0.0.1", 22)
    print(f"    Result: {banner_result}\n")
    
    print("[*] Verification 2: Running live NVD API query for CVE-2021-44228 (Log4Shell)...")
    cve_result = lookup_cve("CVE-2021-44228")
    print(f"    Result Summary:\n{cve_result[:160]}...")

if __name__ == "__main__":
    verify_standalone_tools()