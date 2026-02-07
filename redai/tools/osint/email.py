"""
Email OSINT - Holehe, H8mail integration
"""

import os
import shutil
import subprocess
import requests

from rich.console import Console

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan
from redai.config import settings


console = Console()


def email_osint(email: str, project: str = "General", auto: bool = False):
    """Deep OSINT: Holehe, H8mail and BreachDirectory (Passwords)."""
    display.header(f"Email OSINT: {email}")
    
    results = []
    
    # 1. Holehe
    if shutil.which("holehe"):
        display.step("Running Holehe (account detection)...")
        try:
            proc = subprocess.run(["holehe", email, "--only-used"], capture_output=True, text=True)
            if proc.stdout:
                results.append(f"=== Holehe ===\n{proc.stdout}")
                display.panel(proc.stdout, "Holehe Results", style="cyan")
        except Exception as e:
            display.warning(f"Holehe error: {e}")
    else:
        display.warning("Holehe not installed. Run: pip install holehe")
    
    # 2. BreachDirectory API
    bd_key = settings.breachdirectory_api_key
    if bd_key:
        display.step("Checking BreachDirectory for leaks...")
        try:
            headers = {
                "X-RapidAPI-Key": bd_key,
                "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
            }
            resp = requests.get(
                f"https://breachdirectory.p.rapidapi.com/?func=auto&term={email}",
                headers=headers,
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("found"):
                    breach_info = f"Found in {data.get('sources', [])} breaches"
                    results.append(f"=== BreachDirectory ===\n{breach_info}")
                    display.panel(breach_info, "BreachDirectory", style="red")
                else:
                    display.success("No breaches found in BreachDirectory")
        except Exception as e:
            display.warning(f"BreachDirectory error: {e}")
    
    # 3. H8mail fallback
    if shutil.which("h8mail") and not bd_key:
        display.info("Running h8mail as alternative...")
        try:
            proc = subprocess.run([shutil.which("h8mail"), "-t", email, "-sk"], 
                                  capture_output=True, text=True)
            if proc.stdout:
                results.append(f"=== H8mail ===\n{proc.stdout}")
                display.panel(proc.stdout, "H8mail Output", style="red")
        except:
            pass
    
    # Save combined results
    output = "\n\n".join(results) if results else "No results found."
    suggest_ai_analysis(output, "Email OSINT")
    save_scan(email, "email_osint", output, project)
