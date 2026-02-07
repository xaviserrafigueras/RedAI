"""
Web Directory Fuzzing
"""

import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def fuzz(url: str, project: str = "General", wordlist: str = "common.txt", auto: bool = False):
    """Fuzzing de directorios web (Soporta diccionario personalizado)."""
    if not auto:
        display.header(f"Web Fuzzer: {url}")
    
    if not url.startswith("http"):
        url = f"http://{url}"
    
    # Default wordlist
    targets = [
        "admin", "login", "test", "dev", "backup", "robots.txt", "wp-admin", 
        "dashboard", "api", "config", ".env", "phpinfo.php", ".git", 
        "server-status", "logs", "database"
    ]
    
    # Try to load external wordlist
    if wordlist and os.path.exists(wordlist) and os.path.isfile(wordlist):
        if not auto:
            console.print(f"[green]📂 Loading wordlist: {wordlist}[/green]")
        try:
            with open(wordlist, "r", encoding="latin-1") as f:
                targets = [line.strip() for line in f if line.strip()][:1000]
        except Exception as e:
            display.warning(f"Could not load wordlist: {e}")
    
    found = []
    
    for path in track(targets, description="Fuzzing..."):
        try:
            full_url = f"{url.rstrip('/')}/{path}"
            r = requests.get(full_url, timeout=3, allow_redirects=False)
            
            if r.status_code in [200, 301, 302, 403]:
                status_color = "green" if r.status_code == 200 else "yellow"
                console.print(f"[{status_color}][{r.status_code}] {full_url}[/{status_color}]")
                found.append(f"[{r.status_code}] {full_url}")
                
        except requests.RequestException:
            pass
    
    output = "\n".join(found) if found else "No directories found."
    
    if not auto:
        console.print(Panel(output, title="Fuzzing Results"))
    
    suggest_ai_analysis(output, "Web Fuzzing")
    save_scan(target=url, command_type="fuzz", output=output, project_name=project)
