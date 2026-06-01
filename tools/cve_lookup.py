import urllib.request
import urllib.error
import json
from typing import Dict, Any

def lookup_cve(cve_id: str) -> str:
    """
    Queries the public NVD API for detailed information regarding a specific CVE identifier.
    Does not require an API key for baseline requests.
    """
    print(f"[*] Tool execution: Searching NVD database for {cve_id}...")
    
    # Simple formatting validation to protect our outbound API query string
    if not cve_id.upper().startswith("CVE-"):
        return "Error: Invalid format. CVE identifiers must begin with 'CVE-' (e.g., CVE-2021-44228)."

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id.upper()}"
    
    # Set a professional User-Agent header to prevent aggressive NVD rate limiting blocks
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'CyberGuardAgent/1.0 (Educational Academic Project)'}
    )

    try:
        with urllib.request.urlopen(req, timeout=5.0) as response:
            data = json.loads(response.read().decode())
            
            vulnerabilities = data.get("vulnerabilities", [])
            if not vulnerabilities:
                return f"No results or active mappings found for {cve_id}."
                
            # Extract out the core descriptive text block
            cve_item = vulnerabilities[0].get("cve", {})
            descriptions = cve_item.get("descriptions", [])
            english_desc = next((d["value"] for d in descriptions if d.get("lang") == "en"), "No English description available.")
            
            return f"Vulnerability Details for {cve_id}:\n{english_desc}"
            
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "Error: NVD API rate limited (403 Forbidden). Try again shortly."
        return f"Error: NVD API returned HTTP status code {e.code}."
    except Exception as e:
        return f"Error connecting to NVD CVE registry: {str(e)}"