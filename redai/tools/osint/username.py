"""
Username OSINT - Maigret integration (installed on-demand)
"""

import os
import json

from rich.console import Console
from rich.table import Table
from rich import box

from redai.core.display import display
from redai.core.utils import ensure_tool_installed, suggest_ai_analysis
from redai.core.logger import get_logger
from redai.database.repository import save_scan

import subprocess

console = Console()
logger = get_logger("osint.username")


def username_osint(username: str, project: str = "General", auto: bool = False):
    """Deep Username Search using Maigret (3000+ sites)."""
    display.header("🕵️ Username Recon (Maigret)")
    display.info(f"Searching for user: {username} in 3000+ sites...")
    
    # Check/install maigret
    if not ensure_tool_installed("maigret"):
        display.error("maigret es necesario para esta función. Instálalo manualmente: pip install maigret")
        return
    
    logger.info(f"Starting username OSINT for: {username}")
    
    # Run maigret
    cmd = [
        "maigret",
        username,
        "-a",
        "--json", "simple",
        "--folderoutput", "."
    ]
    
    display.step("Launching Maigret (this can take 5-10 minutes for 3000+ sites)...")
    
    try:
        with console.status("[bold cyan]Scanning cyberspace (Deep Scan)...[/bold cyan]", spinner="earth"):
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        # Find the JSON report
        expected_prefix = f"report_{username}"
        json_file = None
        
        candidates = [f for f in os.listdir('.') if f.startswith(expected_prefix) and f.endswith(".json")]
        if candidates:
            candidates.sort(key=os.path.getmtime, reverse=True)
            json_file = candidates[0]

        if json_file and os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                found_sites = []
                
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, dict):
                            is_found = False
                            final_url = "N/A"
                            
                            if "status" in v and isinstance(v["status"], dict):
                                status_obj = v["status"]
                                if status_obj.get("status") == "Claimed":
                                    is_found = True
                                    final_url = status_obj.get("url_user", v.get("url_user", "N/A"))
                            
                            if not is_found and "url_user" in v and v["url_user"]:
                                is_found = True
                                final_url = v["url_user"]

                            if is_found:
                                found_sites.append({"name": k, "url": final_url})
                
                logger.info(f"Maigret found {len(found_sites)} accounts for {username}")
                
                if found_sites:
                    table = Table(title=f"Accounts Found: {len(found_sites)}", box=box.SIMPLE)
                    table.add_column("Site", style="cyan")
                    table.add_column("URL", style="blue")
                    
                    found_str_list = []
                    
                    for site in found_sites:
                        name = site.get('name', 'Unknown')
                        url = site.get('url', 'N/A')
                        table.add_row(name, f"[link={url}]{url}[/link]")
                        found_str_list.append(f"{name}: {url}")
                        
                    console.print(table)

                    maigret_out = "\n".join(found_str_list)
                    suggest_ai_analysis(f"Maigret found {len(found_sites)} accounts:\n{maigret_out}", "Username Intelligence")
                    save_scan("maigret", "username_scan", maigret_out, project)
                    
                    # Cleanup
                    try:
                        os.remove(json_file)
                    except:
                        pass
                else:
                    display.warning("Maigret executed but found 0 matches.")

            except Exception as e:
                logger.error(f"Error parsing Maigret JSON: {e}")
                display.error(f"Error parsing Maigret JSON: {e}")
        else:
            display.error("Maigret JSON report not found.")
            if proc.stderr:
                display.panel(proc.stderr, "Maigret Error Log", style="red")

    except subprocess.TimeoutExpired:
        display.error("Maigret timeout (10 min). Try with fewer sites.")
    except Exception as e:
        logger.error(f"Username OSINT error: {e}")
        display.error(f"Execution Error: {e}")
