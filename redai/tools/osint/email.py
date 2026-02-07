"""
Email OSINT - Holehe, H8mail, BreachDirectory integration
Holehe is installed on-demand if not present.
"""

import subprocess
import requests

from rich.console import Console
from rich.table import Table
from rich import box

from redai.core.display import display
from redai.core.utils import ensure_tool_installed, suggest_ai_analysis
from redai.core.logger import get_logger
from redai.database.repository import save_scan
from redai.config import settings


console = Console()
logger = get_logger("osint.email")


def email_osint(email: str, project: str = "General", auto: bool = False):
    """Deep OSINT: Holehe (on-demand), H8mail and BreachDirectory."""
    display.header(f"📧 Email OSINT: {email}")
    
    results = []
    
    # 1. Holehe (installed on-demand)
    display.step("Running Holehe (account detection)...")
    
    if ensure_tool_installed("holehe"):
        try:
            logger.info(f"Running holehe for {email}")
            with console.status("[bold cyan]Checking services...[/bold cyan]", spinner="dots"):
                proc = subprocess.run(
                    ["holehe", email, "--only-used"], 
                    capture_output=True, 
                    text=True,
                    timeout=300
                )
            
            if proc.stdout:
                results.append(f"=== Holehe ===\n{proc.stdout}")
                
                # Parse and display as table
                found_services = []
                for line in proc.stdout.split('\n'):
                    if '[+]' in line or '✔' in line:
                        service = line.replace('[+]', '').replace('✔', '').strip()
                        if service:
                            found_services.append(service)
                
                if found_services:
                    table = Table(title=f"Email Found On ({len(found_services)} services)", box=box.ROUNDED)
                    table.add_column("Service", style="cyan")
                    table.add_column("Status", style="green")
                    for svc in found_services:
                        table.add_row(svc, "✅ Registered")
                    console.print(table)
                else:
                    display.panel(proc.stdout, "Holehe Results", style="cyan")
                    
                logger.info(f"Holehe found {len(found_services)} registrations")
        except subprocess.TimeoutExpired:
            display.warning("Holehe timeout (5 min)")
        except Exception as e:
            logger.error(f"Holehe error: {e}")
            display.warning(f"Holehe error: {e}")
    
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
                    display.panel(breach_info, "🔴 BreachDirectory", style="red")
                    logger.info(f"BreachDirectory found breaches for {email}")
                else:
                    display.success("No breaches found in BreachDirectory")
        except Exception as e:
            logger.warning(f"BreachDirectory error: {e}")
            display.warning(f"BreachDirectory error: {e}")
    
    # 3. H8mail fallback (if no BreachDirectory key)
    if not bd_key and ensure_tool_installed("h8mail"):
        display.info("Running h8mail as alternative...")
        try:
            proc = subprocess.run(
                ["h8mail", "-t", email, "-sk"], 
                capture_output=True, 
                text=True,
                timeout=120
            )
            if proc.stdout:
                results.append(f"=== H8mail ===\n{proc.stdout}")
                display.panel(proc.stdout, "H8mail Output", style="red")
        except Exception as e:
            logger.warning(f"H8mail error: {e}")
    
    # Save combined results
    output = "\n\n".join(results) if results else "No results found."
    suggest_ai_analysis(output, "Email OSINT")
    save_scan(email, "email_osint", output, project)
