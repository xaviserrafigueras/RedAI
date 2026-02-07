"""
Google Dorks Generator
"""

from rich.console import Console
from rich.table import Table
from rich import box

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def dork_gen(target: str, project: str = "General", auto: bool = False):
    """Generador de Google Dorks para encontrar archivos sensibles."""
    display.header(f"Google Dorks Generator: {target}")
    
    dorks = [
        ("Directory Listing", f"site:{target} intitle:index.of"),
        ("Config Files", f"site:{target} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini"),
        ("Database Files", f"site:{target} ext:sql | ext:dbf | ext:mdb"),
        ("Log Files", f"site:{target} ext:log"),
        ("Backup Files", f"site:{target} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"),
        ("Login Pages", f'site:{target} inurl:login | inurl:signin | intitle:Login | intitle:"sign in" | inurl:auth'),
        ("SQL Errors", f'site:{target} intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect syntax near"'),
        ("Publicly Exposed Documents", f"site:{target} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv"),
        ("PHP Info", f'site:{target} ext:php intitle:phpinfo "published by the PHP Group"'),
        ("WordPress", f"site:{target} inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download")
    ]
    
    table = Table(title="Google Dorks (Click Link to Open)", box=box.SIMPLE)
    table.add_column("Type", style="cyan")
    table.add_column("Query Link", style="blue")
    
    links = []
    for name, query in dorks:
        link = f"https://www.google.com/search?q={query}"
        table.add_row(name, f"[link={link}]Open Search[/link]")
        links.append(f"{name}: {link}")
        
    console.print(table)
    
    dorks_out = "\n".join(links)
    suggest_ai_analysis(dorks_out, "Google Dorks")
    save_scan(target, "google_dorks", dorks_out, project)
