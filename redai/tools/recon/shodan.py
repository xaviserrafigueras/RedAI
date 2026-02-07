"""
Shodan Intelligence Scanner
"""

import os
import requests
from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan
from redai.config import settings


console = Console()


def shodan_scan(ip: str, project: str = "General", auto: bool = False):
    """Consulta Info de Shodan (Requiere API Key)."""
    if not auto:
        display.header(f"Shodan Intel: {ip}")
    
    api_key = settings.shodan_api_key or os.getenv("SHODAN_API_KEY")
    
    if not api_key:
        display.error("SHODAN_API_KEY not configured. Set it in .env file.")
        return
    
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse relevant info
            info_lines = [
                f"🌐 IP: {data.get('ip_str', 'N/A')}",
                f"🏢 Organization: {data.get('org', 'N/A')}",
                f"📍 Location: {data.get('city', 'N/A')}, {data.get('country_name', 'N/A')}",
                f"🔌 Ports: {', '.join(map(str, data.get('ports', [])))}",
                f"🖥️ OS: {data.get('os', 'N/A')}",
                f"🏷️ Hostnames: {', '.join(data.get('hostnames', []))}",
            ]
            
            # Add vulnerabilities if present
            vulns = data.get('vulns', [])
            if vulns:
                info_lines.append(f"🚨 Vulnerabilities: {', '.join(vulns[:10])}")
            
            output = "\n".join(info_lines)
            
            if not auto:
                console.print(Panel(output, title="Shodan Results", border_style="cyan"))
            
            suggest_ai_analysis(output, "Shodan Intelligence")
            save_scan(target=ip, command_type="shodan", output=output, project_name=project)
            
        elif response.status_code == 404:
            display.warning(f"No Shodan data found for {ip}")
        else:
            display.error(f"Shodan API Error: {response.status_code}")
            
    except Exception as e:
        display.error(f"Shodan Error: {e}")
