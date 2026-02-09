# 🔴 RedAI - Autonomous AI Pentesting Framework

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux)
![AI](https://img.shields.io/badge/AI-Powered-red?style=for-the-badge&logo=openai)

**RedAI Cortex** es un framework de pentesting autónomo potenciado por Inteligencia Artificial.  
Combina más de 25 herramientas de seguridad con un agente de IA que planifica, ejecuta y analiza automáticamente.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## ⚡ Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/xaviserrafigueras/redai.git
cd redai

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key
cp .env.example .env
# Editar .env con tu API key de OpenAI/DeepSeek

# 4. Ejecutar
python main.py
```

---

## 🎯 Features

### 🧠 Agente de IA Autónomo
- Planifica y ejecuta ataques automáticamente
- Analiza resultados y decide siguiente paso
- Genera reportes de hallazgos
- **Multi-proveedor**: OpenAI, DeepSeek, Claude, Ollama (local)

### 🛠️ +25 Herramientas Integradas

| Categoría | Herramientas |
|-----------|--------------| 
| **Recon (1-5)** | Nmap, Shodan, Subdomain Scanner, WordPress, Fuzzing |
| **Exploit (10-16)** | SQLMap, XSS, SearchSploit, Brute Force, Msfvenom |
| **Network (20-25)** | Wi-Fi Audit, Sniffer, ARP Spoofing, Hash Cracker |
| **OSINT (30-35)** | Maigret, TheHarvester, Phone, Email, Metadata |
| **Reporting (40-42)** | HTML, JSON, Markdown Reports |

### ⚙️ Características Avanzadas
- 🎨 **Temas de colores** (default, matrix, ocean, purple, minimal)
- 🔇 **Modos de output** (--quiet, --verbose)
- 📁 **Configuración YAML** flexible
- 🐳 **Docker ready** con Kali Linux
- 📝 **Logging centralizado** con rotación
- 🔄 **Retry automático** en llamadas API
- ✅ **Tests unitarios** incluidos
- 🆕 **Arquitectura modular** - Menú data-driven
- 🆕 **Auto-instalación** de herramientas faltantes

---

## 📦 Installation

### Requisitos
- Python 3.10+
- Kali Linux (recomendado) o Linux
- API key de OpenAI/DeepSeek

### Instalación Manual

```bash
# Clonar
git clone https://github.com/xaviserrafigueras/redai.git
cd redai

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar
cp .env.example .env
nano .env  # Añadir tu OPENAI_API_KEY
```

### 🐳 Docker (Recomendado)

```bash
# Build y ejecutar
docker-compose up -d

# Acceder al contenedor
docker exec -it redai python main.py
```

---

## 🚀 Usage

### Menú Interactivo

```bash
python main.py
```

Esto abre un menú con todas las herramientas disponibles.

### Agente Autónomo (Opción 99)

```bash
# Iniciar agente
python main.py
# Seleccionar opción 99

# El agente te preguntará el objetivo:
> "Escanea la red 192.168.1.0/24 y encuentra vulnerabilidades"
```

### Opciones de línea de comandos

```bash
# Modo silencioso
python main.py --quiet

# Modo debug
python main.py --verbose

# Tema Matrix
python main.py --theme matrix

# Combinado
python main.py -q -t ocean
```

---

## 📚 Documentation

Para documentación detallada, consulta:

- 📖 [**Features Completas**](docs/FEATURES.md) - Lista detallada de todas las herramientas
- 🏗️ [**Arquitectura**](docs/ARCHITECTURE.md) - Cómo funciona internamente
- ⚙️ [**Configuración**](docs/CONFIGURATION.md) - Opciones de config.yaml

---

## 📁 Project Structure

```
redai/
├── ai/                 # Cliente de IA multi-proveedor
│   └── client.py       # OpenAI/DeepSeek/Claude/Ollama
├── core/               # Utilidades centrales
│   ├── display.py      # Sistema de output con temas
│   ├── logger.py       # Logging centralizado
│   ├── utils.py        # Funciones auxiliares
│   ├── menu.py         # 🆕 Menú data-driven (MenuOption)
│   └── handlers.py     # 🆕 Handlers centralizados
├── database/           # Persistencia con SQLModel
│   ├── models.py       # Modelos de datos
│   └── repository.py   # Operaciones CRUD
├── tools/              # Herramientas de pentesting
│   ├── agent.py        # 🧠 Agente autónomo de IA
│   ├── recon/          # Reconocimiento
│   ├── exploit/        # Explotación
│   ├── osint/          # Inteligencia de fuentes abiertas
│   ├── network/        # Herramientas de red
│   └── reporting/      # Generación de reportes
├── config.py           # Configuración + AI_PROVIDERS registry
└── cli.py              # Interfaz de línea de comandos
```

---

## ⚠️ Disclaimer

Esta herramienta es para **uso educativo y pruebas autorizadas únicamente**.

- ⚖️ Úsala solo en sistemas que tengas permiso para probar
- 🔒 El autor no se responsabiliza del mal uso
- 📜 Respeta las leyes de tu país

---

## 📝 License

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

## 🤝 Autor

Desarrollado por **Xavi Serra Figueras**

[![GitHub](https://img.shields.io/badge/GitHub-xaviserrafigueras-181717?style=flat-square&logo=github)](https://github.com/xaviserrafigueras)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-xaviserrafigueras-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/xaviserrafigueras/)

---

<div align="center">

**⭐ Si te gusta el proyecto, dale una estrella ⭐**

</div>
