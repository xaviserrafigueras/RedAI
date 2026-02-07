"""
Network Sniffer - Scapy based
"""

import os

from rich.console import Console

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def sniffer(interface: str = "eth0", count: int = 100, project: str = "General", auto: bool = False):
    """Sniffer de tráfico de red (Scapy)."""
    try:
        display.step("Importing Scapy...")
        from scapy.all import sniff, IP, Raw
    except ImportError:
        display.error("Scapy not installed. Run: pip install scapy")
        return
        
    display.header(f"Network Sniffer [{interface}]", f"Capturing {count} packets...")
    
    captured_summary = []
    
    def pkt_callback(pkt):
        if pkt.haslayer(IP):
            src = pkt[IP].src
            dst = pkt[IP].dst
            proto = pkt[IP].proto
            summary = f"{src} -> {dst} [Proto: {proto}]"
            
            # Check for interesting cleartext
            if pkt.haslayer(Raw):
                try:
                    payload = pkt[Raw].load.decode('utf-8', 'ignore')
                    if any(x in payload for x in ["PASS", "USER", "Authorization", "password"]):
                        summary += f" 🚨 CREDENTIALS? {payload[:50]}"
                        console.print(f"[bold red]{summary}[/bold red]")
                    else:
                        print(f"  {summary} | {payload[:20]}")
                except:
                    print(f"  {summary}")
            else:
                print(f"  {summary}")
                 
            captured_summary.append(summary)

    try:
        if os.name != 'nt' and hasattr(os, 'geteuid') and os.geteuid() != 0:
            display.warning("Sniffing often requires ROOT. Results may be limited.")
            
        sniff(iface=interface, prn=pkt_callback, count=count)
        
        if captured_summary:
            out = "\n".join(captured_summary[:50])
            suggest_ai_analysis(f"Sniffed {len(captured_summary)} packets. Sample:\n{out}", "Network Sniffer")
            save_scan(interface, "net_sniffer", out, project)
            display.success(f"Capture complete. {len(captured_summary)} packets processed.")
            
    except Exception as e:
        display.error(f"Sniffer Error: {e}")
