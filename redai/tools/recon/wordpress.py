"""
WordPress Scanner
"""

import re
import requests
from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def wp_scan(url: str, project: str = "General", auto: bool = False):
    """Enumeración de WordPress."""
    if not auto:
        display.header(f"WordPress Scanner: {url}")
    
    if not url.startswith("http"):
        url = f"http://{url}"
    
    findings = []
    
    try:
        r = requests.get(url, timeout=5)
        
        if "wp-" in r.text:
            findings.append("✔ WP Core Detected")
        
        # Version detection
        v = re.search(r'content="WordPress (.*?)"', r.text)
        if v:
            findings.append(f"⚠️ Version: {v.group(1)}")
        
        # User enumeration via API
        try:
            u = requests.get(f"{url}/wp-json/wp/v2/users", timeout=5)
            if u.status_code == 200:
                users = [x['slug'] for x in u.json()]
                findings.append(f"🚨 Users: {', '.join(users)}")
        except:
            pass
            
        # Check common paths
        common_paths = ["wp-login.php", "wp-admin/", "xmlrpc.php"]
        for path in common_paths:
            try:
                check = requests.get(f"{url}/{path}", timeout=3)
                if check.status_code == 200:
                    findings.append(f"✔ Found: /{path}")
            except:
                pass
                
    except Exception as e:
        findings.append(f"Error: {e}")
    
    out = "\n".join(findings) if findings else "❌ Does not appear to be WordPress."
    
    if not auto:
        console.print(Panel(out, title="WP Scan"))
    
    suggest_ai_analysis(out, "WordPress Scan")
    save_scan(target=url, command_type="wordpress", output=out, project_name=project)
