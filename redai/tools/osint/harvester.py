"""
TheHarvester - Email and Subdomain OSINT
"""

import re
import shutil
import subprocess

from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def harvester_scan(domain: str, limit: int = 500, project: str = "General", auto: bool = False):
    """Recolector de emails y subdominios (TheHarvester)."""
    display.header("TheHarvester: Email & Subdomain OSINT", domain)
    
    if not shutil.which("theHarvester"):
        display.warning("theHarvester is not installed or not in PATH.")
        display.info("Install: sudo apt install theharvester (Kali) or via pip.")
        return

    try:
        sources = "all"
        cmd = ["theHarvester", "-d", domain, "-l", str(limit), "-b", sources]
        
        display.step("Running TheHarvester (this may take a while)...")
        with console.status("[bold green]Harvesting...[/bold green]"):
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
        out = proc.stdout
        
        # Parse basic findings
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", out)
        ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", out)
        
        summary = f"Emails Found: {len(set(emails))}\nIPs Found: {len(set(ips))}"
        display.panel(summary, "Harvester Summary", style="cyan")
        
        if len(out) > 3000:
            console.print(Panel(out[:3000] + "\n... (truncated)", title="Raw Output (Partial)"))
        else:
            console.print(Panel(out, title="Raw Output"))
             
        suggest_ai_analysis(summary + "\n\n[Raw Output Sample]:\n" + out[:2000], "TheHarvester OSINT")
        save_scan(domain, "theharvester", out, project)
        
    except Exception as e:
        display.error(f"Harvester Execution Error: {e}")
