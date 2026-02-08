# ⚙️ RedAI - Guía de Configuración

> Documentación detallada de todas las opciones de configuración

---

## 📁 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `.env` | Variables de entorno sensibles (API keys) |
| `config.yaml` | Configuración de la aplicación |
| `.env.example` | Plantilla para .env |
| `config.example.yaml` | Plantilla para config.yaml |

---

## 🔑 Variables de Entorno (.env)

```bash
# API Keys (REQUERIDO)
OPENAI_API_KEY=sk-...

# Configuración de IA (opcional)
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-chat

# APIs externas (opcional)
SHODAN_API_KEY=...
BREACHDIRECTORY_API_KEY=...
```

### Proveedores de IA Soportados

| Proveedor | AI_BASE_URL | AI_MODEL |
|-----------|-------------|----------|
| OpenAI | `https://api.openai.com/v1` | `gpt-4`, `gpt-3.5-turbo` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Local (LM Studio) | `http://localhost:1234/v1` | (tu modelo) |

---

## 📝 Configuración YAML (config.yaml)

### Estructura Completa

```yaml
# ═══════════════════════════════════════════════════
# Configuración de IA
# ═══════════════════════════════════════════════════
ai:
  # Base URL del API
  base_url: "https://api.deepseek.com/v1"
  
  # Modelo a usar
  model: "deepseek-chat"
  
  # Creatividad (0.0 = determinista, 1.0 = creativo)
  temperature: 0.7
  
  # Máximo tokens por respuesta
  max_tokens: 4000
  
  # Configuración de retry
  retry:
    max_attempts: 3
    min_wait: 2      # segundos
    max_wait: 30     # segundos

# ═══════════════════════════════════════════════════
# Configuración del Agente
# ═══════════════════════════════════════════════════
agent:
  # Máximo de pasos por objetivo
  max_steps: 20
  
  # Timeout de comandos (segundos)
  command_timeout: 120
  
  # Auto-aprobar comandos (¡PELIGROSO!)
  auto_approve: false
  
  # Historial máximo en contexto
  max_history: 15
  
  # Proyecto por defecto
  default_project: "General"

# ═══════════════════════════════════════════════════
# Rutas
# ═══════════════════════════════════════════════════
paths:
  logs: "./logs"
  reports: "./reports"
  database: "./database.db"

# ═══════════════════════════════════════════════════
# APIs Externas
# ═══════════════════════════════════════════════════
apis:
  # shodan_api_key: ""
  # breachdirectory_api_key: ""

# ═══════════════════════════════════════════════════
# Herramientas
# ═══════════════════════════════════════════════════
tools:
  nmap:
    default_args: "-sV -sC"
    timeout: 300
  
  gobuster:
    wordlist: "/usr/share/wordlists/dirb/common.txt"
    timeout: 600
  
  nikto:
    default_args: "-Tuning x 6"
    timeout: 600
  
  sqlmap:
    default_args: "--batch --random-agent"
    timeout: 900
  
  hydra:
    timeout: 1800

# ═══════════════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════════════
logging:
  # Nivel: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: "INFO"
  
  # Log a archivo
  file_enabled: true
  
  # Log a consola
  console_enabled: true
  
  # Retención en días (0 = forever)
  retention_days: 30

# ═══════════════════════════════════════════════════
# Interfaz
# ═══════════════════════════════════════════════════
ui:
  # Mostrar banner al inicio
  show_banner: true
  
  # Tema: default, matrix, ocean, purple, minimal
  theme: "default"
  
  # Modo verbose
  verbose: false
```

---

## 🎨 Temas de Colores

### Uso por CLI

```bash
python main.py --theme matrix
python main.py -t ocean
```

### Temas Disponibles

| Tema | Primary | Secondary | Accent |
|------|---------|-----------|--------|
| `default` | Rojo | Rojo | Cyan |
| `matrix` | Verde | Verde | Verde brillante |
| `ocean` | Azul | Azul | Turquesa |
| `purple` | Púrpura | Magenta | Orquídea |
| `minimal` | Blanco | Blanco | Blanco |

---

## 🔇 Modos de Output

### Uso por CLI

```bash
# Solo errores y resultados
python main.py --quiet
python main.py -q

# Debug completo
python main.py --verbose
python main.py -v
```

### Qué se Muestra en Cada Modo

| Elemento | Quiet | Normal | Verbose |
|----------|-------|--------|---------|
| Banner | ❌ | ✅ | ✅ |
| Headers | ❌ | ✅ | ✅ |
| Paneles | ❌ | ✅ | ✅ |
| Info | ❌ | ✅ | ✅ |
| Steps | ❌ | ✅ | ✅ |
| Debug | ❌ | ❌ | ✅ |
| Warnings | ✅ | ✅ | ✅ |
| Errors | ✅ | ✅ | ✅ |
| Results | ✅ | ✅ | ✅ |

---

## 🐳 Docker

### Variables de Entorno en Docker

```yaml
# docker-compose.yml
services:
  redai:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AI_BASE_URL=${AI_BASE_URL:-https://api.openai.com/v1}
      - AI_MODEL=${AI_MODEL:-gpt-4}
```

### Volúmenes

```yaml
volumes:
  - ./logs:/app/logs
  - ./reports:/app/reports
  - ./database.db:/app/database.db
  - ./config.yaml:/app/config.yaml  # Opcional
```

---

## 🔧 Configuración Rápida

### Para OpenAI

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
AI_MODEL=gpt-4
```

### Para DeepSeek

```bash
# .env
OPENAI_API_KEY=sk-your-deepseek-key
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-chat
```

### Para LM Studio (Local)

```bash
# .env
OPENAI_API_KEY=not-needed
AI_BASE_URL=http://localhost:1234/v1
AI_MODEL=local-model
```
