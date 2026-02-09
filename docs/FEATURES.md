# 📖 RedAI - Features Completas

> Documentación detallada de todas las funcionalidades de RedAI

---

## 📋 Índice

- [Agente Autónomo de IA](#-agente-autónomo-de-ia-redai-cortex)
- [Herramientas de Reconocimiento (1-5)](#-herramientas-de-reconocimiento-1-5)
- [Herramientas de Explotación (10-16)](#️-herramientas-de-explotación-10-16)
- [Herramientas de Red (20-25)](#-herramientas-de-red-20-25)
- [Herramientas OSINT (30-35)](#️-herramientas-osint-30-35)
- [Herramientas de Reporting (40-42)](#-herramientas-de-reporting-40-42)
- [Sistema de Configuración](#️-sistema-de-configuración)
- [Características Avanzadas](#-características-avanzadas)

---

## 🧠 Agente Autónomo de IA (RedAI Cortex)

El corazón de RedAI es su **agente autónomo** que combina inteligencia artificial con herramientas de pentesting para automatizar tareas de seguridad.

### ¿Qué puede hacer?

| Capacidad | Descripción |
|-----------|-------------|
| **Planificar ataques** | Analiza el objetivo y decide qué herramientas usar |
| **Ejecutar comandos** | Corre nmap, sqlmap, gobuster, hydra automáticamente |
| **Analizar resultados** | Interpreta outputs y encuentra vulnerabilidades |
| **Encadenar pasos** | Usa los resultados de un paso para decidir el siguiente |
| **Explicar conceptos** | Responde preguntas como "¿cómo funciona SQLi?" |
| **Generar reportes** | Resume hallazgos con recomendaciones |

### Proveedores de IA Soportados

| Proveedor | Variable .env | Modelos |
|-----------|---------------|---------|
| **OpenAI** | `OPENAI_API_KEY` | gpt-4o-mini, gpt-4, gpt-3.5-turbo |
| **DeepSeek** | `DEEPSEEK_API_KEY` | deepseek-chat, deepseek-coder |
| **Claude** | `CLAUDE_API_KEY` | claude-3-haiku, claude-3-sonnet |
| **Ollama** | (none) | llama3, mistral, codellama |

### Cómo usarlo

```bash
python main.py
# Seleccionar opción 99 (AI Cortex Agent)

# Ejemplos de objetivos:
> "Escanea 192.168.1.1 y encuentra vulnerabilidades"
> "Busca subdominios de example.com y verifica cuáles están activos"
> "¿Cómo funciona un ataque de SQL Injection?"
```

---

## 🔍 Herramientas de Reconocimiento (1-5)

### 1. Nmap Scanner
- **Archivo**: `redai/tools/recon/nmap.py`
- **Descripción**: Escaneo completo de puertos, servicios y versiones

**Funciones:**
- `scan()`: Escaneo completo de un target
- `net_scan()`: Escaneo de red local (descubre hosts)

---

### 2. Shodan Intel
- **Archivo**: `redai/tools/recon/shodan.py`
- **Requiere**: `SHODAN_API_KEY` en `.env`

**Información que obtiene:**
- Puertos abiertos, servicios detectados
- Banners de servicios, vulnerabilidades conocidas

---

### 3. Subdomain Scanner
- **Archivo**: `redai/tools/recon/subdomains.py`

**Técnicas:**
- Consultas a crt.sh (Certificate Transparency)
- Verificación de subdominios activos

---

### 4. WordPress Scanner (WPScan)
- **Archivo**: `redai/tools/recon/wordpress.py`

**Detecta:** Versión WP, plugins vulnerables, usuarios enumerados

---

### 5. Web Fuzzer (Gobuster)
- **Archivo**: `redai/tools/recon/fuzzing.py`

**Características:**
- Usa Gobuster o Dirb
- Wordlists personalizables

---

## ⚔️ Herramientas de Explotación (10-16)

### 10. SQL Injection Scanner (SQLMap)
- **Archivo**: `redai/tools/exploit/sqli.py`

**Capacidades:**
- Detección automática de SQLi
- Dump de bases de datos
- Bypass de WAF (--tamper)

---

### 11. XSS Scanner
- **Archivo**: `redai/tools/exploit/xss.py`

**Características:**
- Múltiples vectores de ataque
- Detección de XSS reflejado
- Bypass de filtros comunes

---

### 12. SearchSploit (Exploit-DB)
- **Archivo**: `redai/tools/exploit/exploits.py`

**Base de datos:** 40,000+ exploits, POCs, shellcodes

---

### 13. Brute Force (Hydra)
- **Archivo**: `redai/tools/exploit/bruteforce.py`

**Protocolos:** SSH, FTP, HTTP, SMB, RDP, MySQL, etc.

---

### 14. Msfvenom Payload Generator
- **Archivo**: `redai/tools/exploit/payload.py`

**Plataformas:** Windows, Linux, Web (php, jsp)
**Payloads:** Reverse shell, bind shell, meterpreter

---

### 15. Phishing Templates
- **Archivo**: `redai/tools/reporting/phishing.py`

**Templates:** Google, Microsoft, Netflix, PayPal

---

### 16. Subdomain Takeover
- **Archivo**: `redai/tools/recon/subdomains.py`

**Detecta:** AWS S3, GitHub Pages, Heroku, Azure, Shopify

---

## 🌐 Herramientas de Red (20-25)

### 20. Wi-Fi Auditor
- **Archivo**: `redai/tools/network/wifi.py`
- **Requiere**: Adaptador Wi-Fi compatible

**Funciones:** Escaneo, deauth attack, captura handshakes

---

### 21. Wi-Fi Password Dump
- **Archivo**: `redai/tools/network/wifi.py`

Extrae contraseñas Wi-Fi guardadas en el sistema local.

---

### 22. Packet Sniffer
- **Archivo**: `redai/tools/network/sniffer.py`
- **Requiere**: Root/sudo

**Características:** Captura en tiempo real, filtrado, exportación PCAP

---

### 23. ARP Spoofing (MITM)
- **Archivo**: `redai/tools/network/arp.py`
- **Requiere**: Root/sudo

**Modos:** MITM (interceptar) o Kick (desconectar)

---

### 24. Network Scanner
- **Archivo**: `redai/tools/recon/nmap.py`

Escaneo de subredes para descubrir hosts activos.

---

### 25. Hash Cracker
- **Archivo**: `redai/tools/exploit/crack.py`

**Algoritmos:** MD5, SHA1, SHA256, SHA512, NTLM, bcrypt

---

## 🕵️ Herramientas OSINT (30-35)

### 30. Exif Spy (Metadata Extractor)
- **Archivo**: `redai/tools/osint/metadata.py`

**Extrae:** GPS, modelo de cámara, fecha, software usado

---

### 31. Username Recon (Maigret)
- **Archivo**: `redai/tools/osint/username.py`
- **Instalación**: Automática bajo demanda

Busca username en 3000+ sitios web.

---

### 32. Phone OSINT
- **Archivo**: `redai/tools/osint/phone.py`

**Info:** País, operadora, tipo de línea, zona horaria

---

### 33. Google Dorks Generator
- **Archivo**: `redai/tools/osint/dorks.py`

**Genera dorks para:** SQL expuestos, backups, admin panels

---

### 34. Metadata FOCA
- **Archivo**: `redai/tools/osint/metadata.py`

Extracción profunda de metadatos en documentos (PDF, DOCX).

---

### 35. TheHarvester
- **Archivo**: `redai/tools/osint/harvester.py`

**Recolecta:** Emails, subdominios, hosts, IPs

---

## 📊 Herramientas de Reporting (40-42)

### 40. HTML Report Generator
- **Archivo**: `redai/tools/reporting/html.py`

Diseño profesional, responsive, estilo cyberpunk.

---

### 41. JSON Export
- **Archivo**: `redai/tools/reporting/json_report.py`

Formato estructurado para integración con APIs.

---

### 42. Markdown Export
- **Archivo**: `redai/tools/reporting/markdown.py`

Ideal para documentación en GitHub/GitLab.

---

## ⚙️ Sistema de Configuración

### Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `.env` | Variables de entorno sensibles (API keys) |
| `config.yaml` | Configuración de la aplicación |

### Configuración Rápida Multi-Provider

```bash
# OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...

# DeepSeek (más barato)
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-...

# Ollama (local, gratis)
AI_PROVIDER=ollama
AI_MODEL=llama3
```

---

## 🚀 Características Avanzadas

### 🎨 Temas de Colores

| Tema | Estilo |
|------|--------|
| `default` | Cyberpunk/Hacker (Rojo, Cyan) |
| `matrix` | Matrix clásica (Verde neón) |
| `ocean` | Profesional (Azul, Turquesa) |
| `purple` | Moderno (Púrpura, Magenta) |
| `minimal` | Sin color (Blanco, Gris) |

```bash
python main.py --theme matrix
```

---

### 🔇 Modos de Output

| Modo | Flag | Qué se muestra |
|------|------|----------------|
| Normal | (default) | Todo |
| Quiet | `-q, --quiet` | Solo errores y resultados |
| Verbose | `-v, --verbose` | Todo + debug |

---

### 🆕 Arquitectura Modular

El menú interactivo usa un sistema **data-driven**:

- `redai/core/menu.py` - Definición de opciones (`MenuOption`)
- `redai/core/handlers.py` - Handlers centralizados

**Añadir nueva herramienta = 1 línea en `menu.py`**

---

### 🔄 Auto-instalación de Herramientas

Cuando una herramienta no está instalada:
```
⚠️ sublist3r no está instalado.
¿Instalar sublist3r ahora? [Y/n]
```

---

### 🐳 Docker

```bash
docker-compose up -d
docker exec -it redai python main.py
```

**Imagen base:** Kali Linux Rolling
**Herramientas preinstaladas:** nmap, gobuster, sqlmap, hydra, nikto
