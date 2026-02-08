"""
Subdomain Enumeration and Takeover Detection
"""

import subprocess
import shutil

import dns.resolver
from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis, ensure_tool_installed
from redai.database.repository import save_scan


console = Console()


def subdomains(domain: str, project: str = "General", auto: bool = False):
    """Reconocimiento pasivo de subdominios."""
    display.header(f"Subdomain Enumeration ({domain})")
    
    try:
        display.step(f"Searching subdomains for {domain}...")
        
        # Check and offer to install if missing
        if not ensure_tool_installed("sublist3r", "sublist3r"):
            return

        cmd = ["sublist3r", "-d", domain, "-t", "10", "-n"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        output = proc.stdout + proc.stderr
        display.panel(output, f"Subdomains: {domain}")
        
        suggest_ai_analysis(output, "Subdomain Enumeration")
        save_scan(target=domain, command_type="subdomains", output=output, project_name=project)

    except Exception as e:
        display.error(f"Error: {e}")


def sub_takeover(domain: str, project: str = "General", auto: bool = False):
    """Verificación de vulnerabilidad Subdomain Takeover."""
    if not auto:
        display.tool_info("takeover")
    display.header(f"Subdomain Takeover Check: {domain}")
    
    vuln_signatures = {
        "github.io": "GitHub Pages",
        "herokuapp.com": "Heroku",
        "s3.amazonaws.com": "AWS S3",
        "bitbucket.org": "Bitbucket",
        "azurewebsites.net": "Azure App",
        "ghost.io": "Ghost",
        "pantheon.io": "Pantheon",
        "myshopify.com": "Shopify",
        "tumblr.com": "Tumblr",
        "wordpress.com": "WordPress",
    }

    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        out_msg = ""
        vulnerable = False
        
        for rdata in answers:
            cname = str(rdata.target)
            display.info(f"CNAME found: {cname}")
            
            for sig, platform in vuln_signatures.items():
                if sig in cname:
                    msg = f"🚨 POTENTIAL TAKEOVER: {domain} -> {cname} ({platform})"
                    console.print(Panel(msg, style="bold red"))
                    out_msg += msg + "\n"
                    vulnerable = True
                    break
            
            if not vulnerable:
                out_msg += f"CNAME: {cname} (No known takeover signature detected)\n"

        if not vulnerable:
            display.success(f"{domain} seems safe (CNAME check).")
            
        save_scan(domain, "sub_takeover", out_msg, project)

    except dns.resolver.NoAnswer:
        display.warning("No CNAME record found.")
    except Exception as e:
        display.error(f"DNS Error: {e}")
