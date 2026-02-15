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

### Acciones del Agente

El agente responde siempre en formato JSON con una de estas acciones:

```json
{
    "thought": "Mi razonamiento sobre qué hacer...",
    "action": "execute|analyze|explain|ask|complete",
    "command": "nmap -sV target",
    "explanation": "Por qué ejecuto esto...",
    "findings": ["Hallazgo 1", "Hallazgo 2"],
    "recommendations": ["Recomendación 1"]
}
```

| Acción | Cuándo se usa |
|--------|---------------|
| `execute` | Ejecuta un comando de terminal |
| `analyze` | Analiza resultados y planifica siguiente paso |
| `explain` | Explica un concepto de ciberseguridad (cuando preguntas "cómo", "qué") |
| `ask` | Pide más información al usuario |
| `complete` | Finaliza el objetivo con resumen de hallazgos |

### Cómo usarlo

```bash
python main.py
# Seleccionar opción 99 (AI Cortex Agent)

# Ejemplos de objetivos:
> "Escanea 192.168.1.1 y encuentra vulnerabilidades"
> "Busca subdominios de example.com y verifica cuáles están activos"
> "¿Cómo funciona un ataque de SQL Injection?"
```

### Memoria de Sesión

El agente mantiene un historial de la conversación para contexto:
- Recuerda comandos ejecutados anteriormente
- Mantiene los hallazgos entre pasos
- Puede referenciar resultados previos

---

## 🔍 Herramientas de Reconocimiento (1-5)

### Opción 1: Nmap Scanner
- **Archivo**: `redai/tools/recon/nmap.py`
- **Descripción**: Escaneo completo de puertos, servicios y versiones

**Funciones:**
- `scan()`: Escaneo completo de un target
- `net_scan()`: Escaneo de red local (descubre hosts)

**Ejemplo de uso:**
```bash
# Desde el menú
Opción 1 → Introducir IP/dominio

# Comandos que ejecuta
nmap -sV -sC -A <target>
nmap -sn 192.168.1.0/24  # Para net_scan
```

---

### Opción 2: Shodan Intel
- **Archivo**: `redai/tools/recon/shodan.py`
- **Requiere**: `SHODAN_API_KEY` en `.env`

**Información que obtiene:**
- Puertos abiertos
- Servicios detectados
- Banners de servicios
- Vulnerabilidades conocidas
- Información del ISP

---

### Opción 3: Subdomain Scanner
- **Archivo**: `redai/tools/recon/subdomains.py`

**Técnicas utilizadas:**
- Consultas a crt.sh (Certificate Transparency)
- DNS brute force opcional
- Verificación de subdominios activos
- **Auto-instalación**: Si falta sublist3r, ofrece instalarlo

---

### Opción 4: WordPress Scanner (WPScan)
- **Archivo**: `redai/tools/recon/wordpress.py`
- **Requiere**: wpscan instalado

**Detecta:**
- Versión de WordPress
- Plugins instalados y vulnerables
- Temas vulnerables
- Usuarios enumerados
- XML-RPC habilitado

---

### Opción 5: Web Fuzzer (Directory Discovery)
- **Archivo**: `redai/tools/recon/fuzzing.py`

**Características:**
- Usa Gobuster o Dirb
- Wordlists personalizables
- Filtrado por códigos de respuesta
- Detección de archivos de backup

---

## ⚔️ Herramientas de Explotación (10-16)

### Opción 10: SQL Injection Scanner (SQLMap)
- **Archivo**: `redai/tools/exploit/sqli.py`
- **Requiere**: sqlmap instalado

**Capacidades:**
- Detección automática de SQLi
- Dump de bases de datos
- Extracción de tablas y columnas
- Bypass de WAF (--tamper)
- Múltiples técnicas: UNION, Error-based, Blind, Time-based

**Ejemplo:**
```bash
sqlmap -u "http://target.com/page?id=1" --dbs --batch
```

---

### Opción 11: XSS Scanner
- **Archivo**: `redai/tools/exploit/xss.py`

**Características:**
- Múltiples vectores de ataque
- Detección de XSS reflejado
- Payloads personalizables
- Bypass de filtros comunes

---

### Opción 12: SearchSploit (Exploit-DB)
- **Archivo**: `redai/tools/exploit/exploits.py`
- **Requiere**: searchsploit instalado

**Base de datos:**
- 40,000+ exploits
- Pruebas de concepto
- Shellcodes
- Papers técnicos

---

### Opción 13: Brute Force (Hydra)
- **Archivo**: `redai/tools/exploit/bruteforce.py`
- **Requiere**: hydra instalado

**Protocolos soportados:**
- SSH, FTP, Telnet
- HTTP/HTTPS (Basic, Form)
- SMB, RDP
- MySQL, PostgreSQL
- Y más...

---

### Opción 14: Msfvenom Payload Generator
- **Archivo**: `redai/tools/exploit/payload.py`
- **Requiere**: msfvenom (Metasploit)

**Plataformas:**
- Windows (exe, dll)
- Linux (elf)
- Web (php, jsp, asp)
- Python, Perl, Ruby

**Tipos de payload:**
- Reverse shell
- Bind shell
- Meterpreter

---

### Opción 15: Phishing Templates
- **Archivo**: `redai/tools/reporting/phishing.py`

**Templates incluidos:**
- Google Login
- Microsoft 365
- Netflix
- PayPal
- Apple ID
- Instagram
- Personalizable

**Uso:** Pruebas de concienciación (phishing simulado)

---

### Opción 16: Subdomain Takeover Checker
- **Archivo**: `redai/tools/recon/subdomains.py`

**Detecta subdominios vulnerables en:**
- AWS S3 / CloudFront
- GitHub Pages
- Heroku
- Azure
- Shopify
- Y más...

---

## 🌐 Herramientas de Red (20-25)

### Opción 20: Wi-Fi Auditor
- **Archivo**: `redai/tools/network/wifi.py`
- **Requiere**: Adaptador Wi-Fi compatible + root/sudo

**Funciones:**
- Escaneo de redes
- Deauthentication attack
- Captura de handshakes WPA/WPA2
- Cracking de contraseñas

---

### Opción 21: Wi-Fi Password Dump
- **Archivo**: `redai/tools/network/wifi.py`

**Extrae contraseñas Wi-Fi guardadas en el sistema local.**
- Funciona en Linux (NetworkManager)
- Muestra SSID y contraseña

---

### Opción 22: Network Sniffer
- **Archivo**: `redai/tools/network/sniffer.py`
- **Requiere**: Root/sudo

**Características:**
- Captura en tiempo real
- Filtrado por protocolo
- Exportación a PCAP
- Análisis de paquetes

---

### Opción 23: ARP Spoofing (MITM)
- **Archivo**: `redai/tools/network/arp.py`
- **Requiere**: Root/sudo

**Modos:**
- **MITM**: Interceptar tráfico entre víctima y gateway
- **Kick**: Desconectar dispositivo de la red

---

### Opción 24: Network Scanner
- **Archivo**: `redai/tools/recon/nmap.py`

**Escaneo de redes locales:**
- Descubrimiento de hosts activos
- Identificación de dispositivos
- Detección de servicios

---

### Opción 25: Hash Cracker
- **Archivo**: `redai/tools/exploit/crack.py`

**Algoritmos soportados:**
- MD5, SHA1, SHA256, SHA512
- NTLM, LM
- bcrypt, scrypt

**Métodos:**
- Diccionario (wordlist)
- Fuerza bruta
- Rainbow tables

---

## 🕵️ Herramientas OSINT (30-35)

### Opción 30: Exif Spy (Metadata de Imágenes)
- **Archivo**: `redai/tools/osint/metadata.py`

**Extrae metadatos de imágenes:**
- Coordenadas GPS
- Modelo de cámara
- Fecha de creación
- Software usado

---

### Opción 31: Username Recon (Maigret)
- **Archivo**: `redai/tools/osint/username.py`
- **Instalación**: Bajo demanda (se instala automáticamente)

**Capacidades:**
- Busca username en 3000+ sitios
- Genera reportes HTML/JSON
- Muestra perfiles encontrados con URLs

---

### Opción 32: Phone OSINT
- **Archivo**: `redai/tools/osint/phone.py`

**Información extraída:**
- País de origen
- Operadora/carrier
- Tipo de línea (móvil/fijo)
- Zona horaria
- Formato internacional

---

### Opción 33: Google Dorks Generator
- **Archivo**: `redai/tools/osint/dorks.py`

**Genera dorks para encontrar:**
- Archivos SQL expuestos
- Logs de configuración
- Backups (.bak, .old)
- Paneles de admin
- Archivos de configuración

---

### Opción 34: Metadata FOCA
- **Archivo**: `redai/tools/osint/metadata.py`

**Extrae metadatos de:**
- Imágenes (JPEG, PNG, TIFF)
- Documentos (PDF, DOCX)
- Archivos multimedia

**Información obtenida:**
- Autor/creador
- Software usado
- Fechas de modificación
- Rutas de archivos

---

### Opción 35: TheHarvester
- **Archivo**: `redai/tools/osint/harvester.py`
- **Auto-instalación**: Ofrece instalar si falta

**Recolecta:**
- Emails asociados a un dominio
- Subdominios
- Nombres de hosts
- IPs
- URLs

**Fuentes utilizadas:**
- Google, Bing, Baidu
- LinkedIn, Twitter
- DNSdumpster
- Shodan
- CRT.sh

---

## 📊 Herramientas de Reporting (40-42)

### Opción 40: HTML Report Generator
- **Archivo**: `redai/tools/reporting/html.py`

**Características:**
- Diseño profesional y responsive
- Gráficos de resumen
- Timeline de eventos
- Estilo cyberpunk/hacker
- Exporta a archivo HTML standalone
- **Guarda en**: `reports/{proyecto}/`

---

### Opción 41: JSON Export
- **Archivo**: `redai/tools/reporting/json_report.py`

**Formato estructurado para:**
- Integración con APIs
- Automatización
- Procesamiento posterior
- Importación en otras herramientas
- **Guarda en**: `reports/{proyecto}/`

---

### Opción 42: Markdown Export
- **Archivo**: `redai/tools/reporting/markdown.py`

**Ideal para:**
- Documentación en GitHub/GitLab
- Wikis internas
- Notas de pentesting
- Reportes legibles
- **Guarda en**: `reports/{proyecto}/`

---

## ⚙️ Sistema de Configuración

### Archivos de Configuración

| Archivo | Propósito |
|---------|-----------| 
| `.env` | Variables de entorno sensibles (API keys) |
| `config.yaml` | Configuración de la aplicación |
| `.env.example` | Plantilla para .env |
| `config.example.yaml` | Plantilla para config.yaml |

### Prioridades de Configuración

```
1. Variables de Entorno (.env)  ← Máxima prioridad
2. config.yaml                  ← Segunda prioridad
3. Valores por defecto          ← Si no hay nada más
```

### Ejemplo de config.yaml

```yaml
# Configuración de IA
ai:
  provider: "openai"    # openai, deepseek, claude, ollama
  model: "gpt-4o-mini"
  temperature: 0.7
  max_tokens: 4000

# Configuración del Agente
agent:
  max_steps: 20
  command_timeout: 120
  auto_approve: false

# Interfaz
ui:
  theme: "default"
  show_banner: true

# Logging
logging:
  level: "INFO"
  file_enabled: true
```

### Variables de Entorno

```bash
# Selección de proveedor IA
AI_PROVIDER=openai  # openai, deepseek, claude, ollama

# API Keys por proveedor
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...

# Modelo (opcional, usa default del provider)
AI_MODEL=gpt-4o-mini

# APIs externas (opcionales)
SHODAN_API_KEY=...
BREACHDIRECTORY_API_KEY=...
```

### Proveedores de IA Soportados (Multi-Provider)

RedAI soporta múltiples proveedores de IA con configuración simplificada:

| Proveedor | Variable .env | Modelos | Notas |
|-----------|---------------|---------|-------|
| **OpenAI** | `OPENAI_API_KEY` | gpt-4o-mini, gpt-4, gpt-3.5-turbo | Default |
| **DeepSeek** | `DEEPSEEK_API_KEY` | deepseek-chat, deepseek-coder | Más barato |
| **Claude** | `CLAUDE_API_KEY` | claude-3-haiku, claude-3-sonnet | Anthropic |
| **Ollama** | (none) | llama3, mistral, codellama | Local y gratis |

**Configuración rápida:**
```bash
# .env - Solo cambia el provider!
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-key
```

La URL base y modelo por defecto se auto-configuran según el provider.

---

## 🚀 Características Avanzadas

### 🎨 Temas de Colores

RedAI incluye 5 temas de colores:

| Tema | Estilo | Colores principales |
|------|--------|---------------------|
| `default` | Cyberpunk/Hacker | Rojo, Cyan, Amarillo |
| `matrix` | Matrix clásica | Verde neón |
| `ocean` | Profesional | Azul, Turquesa |
| `purple` | Moderno | Púrpura, Magenta |
| `minimal` | Sin color | Blanco, Gris |

```bash
python main.py --theme matrix
python main.py -t ocean
```

---

### 🔇 Modos de Output

| Modo | Flag | Qué se muestra |
|------|------|----------------|
| Normal | (default) | Todo |
| Quiet | `-q, --quiet` | Solo errores y resultados finales |
| Verbose | `-v, --verbose` | Todo + mensajes de debug |

```bash
python main.py --quiet
python main.py --verbose
python main.py -q -t minimal  # Combinado
```

---

### 📝 Sistema de Logging

- **Ubicación**: `logs/redai_YYYYMMDD.log`
- **Rotación**: Diaria (nuevo archivo cada día)
- **Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Qué se registra:**
- Inicio/fin de sesiones
- Comandos ejecutados
- Errores y excepciones
- Llamadas a la API
- Resultados de herramientas

---

### 🔄 Retry Automático (Tenacity)

Las llamadas a la API de IA tienen reintentos automáticos:
- **Intentos máximos**: 3
- **Backoff exponencial**: 2s → 4s → 8s
- **Registra**: Cada intento en los logs

---

### 🐳 Docker

RedAI incluye soporte completo para Docker:

```bash
# Build
docker-compose build

# Ejecutar en segundo plano
docker-compose up -d

# Acceder al contenedor
docker exec -it redai python main.py

# Ver logs
docker-compose logs -f
```

**Imagen base:** Kali Linux Rolling
**Herramientas preinstaladas:** nmap, gobuster, sqlmap, hydra, nikto, wpscan

---

### 🧪 Tests Unitarios

```bash
# Ejecutar todos los tests
pytest tests/

# Con reporte de cobertura
pytest tests/ --cov=redai

# Modo verbose
pytest tests/ -v
```

**Tests incluidos:**
- `test_agent.py`: Parseo de respuestas del agente IA
- `test_utils.py`: Funciones de utilidad, validación de inputs

---

### 🗄️ Base de Datos

- **Motor**: SQLite con SQLModel
- **Archivo**: `database.db`

**Modelos:**

| Modelo | Descripción |
|--------|-------------|
| `ScanRecord` | Resultados de escaneos (target, tipo, output, proyecto) |
| `AgentStep` | Pasos del agente (thought, action, command, findings) |

---

### 🆕 Arquitectura Modular del Menú

El menú de RedAI usa un sistema **data-driven**:

```python
# redai/core/menu.py - Define todas las opciones
MENU_OPTIONS = [
    MenuOption(id="1", name="Nmap Scanner", category="recon", ...),
    MenuOption(id="2", name="Shodan Intel", category="recon", ...),
    # ...
]

# redai/core/handlers.py - Ejecuta cada opción
HANDLERS = {
    "handle_nmap": handle_nmap,
    "handle_shodan": handle_shodan,
    # ...
}
```


**Beneficios:**
- Añadir herramientas = 1 línea en `menu.py`
- Menú se auto-genera desde datos
- Fácil mantenimiento

---

### 🔧 Auto-Instalación de Herramientas

Cuando falta una herramienta requerida, RedAI ofrece instalarla:

```
⚠️ sublist3r no está instalado.
¿Instalar sublist3r ahora? [Y/n]
```

Compatible con:
- sublist3r
- maigret
- theHarvester
- Y más...

---

### 🐧 Detección de SO

Al iniciar, RedAI detecta el sistema operativo:
- En **Linux/Kali**: Funciona completamente
- En **Windows/Mac**: Muestra aviso de compatibilidad

---

### 🔒 Seguridad

- **shell=False**: Los comandos se ejecutan sin shell para evitar inyección
- **shlex.split()**: Parsing seguro de comandos
- **Instalación bajo demanda**: Maigret/Holehe solo se instalan cuando se necesitan

---

## 📋 Resumen de Opciones del Menú

| Categoría | IDs | Herramientas |
|-----------|-----|--------------|
| **Recon** | 1-5 | Nmap, Shodan, Subdomains, WordPress, Fuzzing |
| **Exploit** | 10-16 | SQLi, XSS, SearchSploit, Brute, Msfvenom, Phishing, Takeover |
| **Network** | 20-25 | Wi-Fi, Wi-Fi Dump, Sniffer, ARP, NetScan, Hash |
| **OSINT** | 30-35 | Exif, Username, Phone, Dorks, Metadata, Harvester |
| **Reporting** | 40-42 | HTML, JSON, Markdown |
| **Special** | 99 | 🧠 RED AI CORTEX |
