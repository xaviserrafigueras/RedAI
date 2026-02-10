"""
Tool descriptions for the help system.
Separated from config.py to avoid circular imports.
"""

TOOL_DESCRIPTIONS = {
    # Recon Tools
    "nmap": "Escáner de red para descubrir hosts y servicios abiertos. Uso: nmap -sV -sC <target>.",
    "shodan": "Motor de búsqueda de dispositivos conectados (IoT, Servidores). Requiere API Key.",
    "subdomains": "Enumeración de subdominios usando herramientas como Sublist3r, Amass y DNS brute-force.",
    "wordpress": "Escáner especializado en WordPress (plugins, temas, usuarios).",
    "wpscan": "Escáner especializado en WordPress (plugins, temas, usuarios).",
    "fuzz": "Fuzzing de directorios y archivos web usando diccionarios (gobuster, dirbuster).",
    "gobuster": "Fuzzer de directorios y subdominios usando diccionarios.",
    
    # Exploit Tools
    "sqli": "Detección y explotación automática de SQL Injection en aplicaciones web.",
    "sqlmap": "Herramienta automática de SQL Injection. Detecta y explota vulns DB.",
    "xss": "Escáner de vulnerabilidades XSS (Cross-Site Scripting) en páginas web.",
    "searchsploit": "Búsqueda local de exploits en la base de datos de Exploit-DB.",
    "brute": "Ataque de fuerza bruta contra servicios de autenticación (SSH, FTP, HTTP).",
    "hydra": "Cracker de fuerza bruta para protocolos (SSH, FTP, HTTP, etc.).",
    "msfvenom": "Generador de payloads de Metasploit (reverse shells, meterpreter, etc.).",
    "metasploit": "Framework de explotación con miles de exploits y payloads.",
    "phishing": "Generador de plantillas de phishing realistas (Google, Microsoft, Netflix, PayPal).",
    "takeover": "Detección de subdominios vulnerables a takeover (GitHub Pages, AWS S3, etc.).",
    
    # Network Tools
    "wifi": "Gestión de perfiles Wi-Fi guardados y ataques de desautenticación.",
    "wifite": "Auditoría automatizada de redes Wi-Fi (WEP, WPA, WPS).",
    "aircrack-ng": "Suite completa para hackear redes Wi-Fi.",
    "sniffer": "Captura y análisis de tráfico de red en tiempo real (Scapy).",
    "arp": "Ataque MITM (ARP Spoofing) para interceptar tráfico o cortar internet (Kick).",
    "dns": "DNS Spoofing para redirigir tráfico de dominios legítimos a una IP maliciosa.",
    "hash": "Cracker de hashes con diccionarios y rainbow tables (hashcat, john).",
    "hashcat": "Cracker de hashes GPU-accelerated. Soporta MD5, SHA, NTLM, etc.",
    
    # OSINT Tools
    "exif": "Extracción de metadatos EXIF de imágenes (GPS, cámara, software, etc.).",
    "maigret": "Rastreo de nombre de usuario en 3000+ sitios web (OSINT).",
    "phone": "Inteligencia de números telefónicos (Operadora, País, Zona Horaria).",
    "harvester": "Recolector de emails, subdominios y hosts (TheHarvester).",
    "dorks": "Generador de Google Dorks para encontrar archivos sensibles y paneles.",
    "metadata": "Extracción profunda de metadatos en documentos y archivos (PDF, DOC, IMG).",
    
    # Reporting Tools
    "html": "Generador de reportes HTML profesionales con gráficos y tablas de hallazgos.",
    "json": "Exportación de resultados a formato JSON para integración con otras herramientas.",
    "markdown": "Generador de reportes en Markdown para documentación técnica.",
    
    # Special
    "agent": "🧠 Agente autónomo de IA que planifica y ejecuta ataques de pentesting de forma inteligente.",
    
    # Legacy compatibility
    "nikto": "Escáner de vulnerabilidades web (misconfigs, archivos peligrosos).",
}
