# 🏗️ RedAI - Arquitectura

> Documentación técnica de la estructura interna de RedAI

---

## 📁 Estructura del Proyecto

```
redai/
├── main.py                 # Entry point
├── requirements.txt        # Dependencias Python
├── config.example.yaml     # Plantilla de configuración
├── Dockerfile              # Imagen Docker
├── docker-compose.yml      # Orquestación
│
├── redai/                  # Paquete principal
│   ├── __init__.py
│   ├── cli.py              # Interfaz de línea de comandos (Typer)
│   ├── config.py           # Sistema de configuración
│   │
│   ├── ai/                 # Módulo de IA
│   │   ├── client.py       # Cliente OpenAI/DeepSeek con retry
│   │   └── cortex.py       # Funciones auxiliares de IA
│   │
│   ├── core/               # Utilidades centrales
│   │   ├── display.py      # Output con Rich + temas
│   │   ├── logger.py       # Logging centralizado
│   │   └── utils.py        # Funciones auxiliares
│   │
│   ├── database/           # Persistencia
│   │   ├── models.py       # Modelos SQLModel
│   │   └── repository.py   # Operaciones CRUD
│   │
│   └── tools/              # Herramientas de pentesting
│       ├── agent.py        # 🧠 Agente autónomo
│       ├── base.py         # Clase base para tools
│       ├── recon/          # Reconocimiento
│       ├── exploit/        # Explotación
│       ├── osint/          # Inteligencia
│       ├── network/        # Red
│       └── reporting/      # Reportes
│
├── tests/                  # Tests unitarios
│   ├── conftest.py         # Fixtures
│   ├── test_agent.py
│   └── test_utils.py
│
├── docs/                   # Documentación
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   └── CONFIGURATION.md
│
└── logs/                   # Logs (generado)
```

---

## 🔄 Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                            │                                    │
│                            ▼                                    │
│                        cli.py                                   │
│                   (Typer CLI App)                               │
│                            │                                    │
│              ┌─────────────┴─────────────┐                      │
│              ▼                           ▼                      │
│      interactive_menu()            Subcommands                  │
│              │                                                  │
│              ▼                                                  │
│    ┌─────────────────┐                                          │
│    │  User selects   │                                          │
│    │    option 99    │──────────▶ agent.py (AI Agent)           │
│    │   (or 1-27)     │                    │                     │
│    └─────────────────┘                    ▼                     │
│              │                    ┌───────────────┐             │
│              ▼                    │   AI Client   │             │
│    ┌─────────────────┐            │  (with retry) │             │
│    │  Specific Tool  │            └───────────────┘             │
│    │   (nmap, etc)   │                    │                     │
│    └─────────────────┘                    ▼                     │
│              │                    ┌───────────────┐             │
│              ▼                    │ Parse JSON    │             │
│    ┌─────────────────┐            │   Response    │             │
│    │ Execute Command │◀───────────┴───────────────┘             │
│    │  (subprocess)   │                                          │
│    └─────────────────┘                                          │
│              │                                                  │
│              ▼                                                  │
│    ┌─────────────────┐                                          │
│    │  Save to DB     │                                          │
│    │  (SQLModel)     │                                          │
│    └─────────────────┘                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Agente de IA - Arquitectura

### Ciclo del Agente

```
┌────────────────────────────────────────────────────────────────┐
│                        AGENT LOOP                              │
│                                                                │
│   ┌─────────┐    ┌─────────────┐    ┌──────────────┐          │
│   │  User   │───▶│   System    │───▶│   AI Model   │          │
│   │ Objective│    │   Prompt    │    │ (DeepSeek/   │          │
│   └─────────┘    │ + History   │    │  OpenAI)     │          │
│                  └─────────────┘    └──────────────┘          │
│                                            │                   │
│                                            ▼                   │
│                                    ┌──────────────┐           │
│                                    │ Parse JSON   │           │
│                                    │  Response    │           │
│                                    └──────────────┘           │
│                                            │                   │
│         ┌──────────────────────────────────┼──────────────┐   │
│         ▼              ▼                   ▼              ▼   │
│   ┌──────────┐  ┌──────────┐        ┌──────────┐   ┌────────┐│
│   │ execute  │  │ analyze  │        │ explain  │   │complete││
│   │ command  │  │ results  │        │ concept  │   │ task   ││
│   └──────────┘  └──────────┘        └──────────┘   └────────┘│
│         │              │                   │              │   │
│         └──────────────┴───────────────────┘              │   │
│                        │                                  │   │
│                        ▼                                  │   │
│                 ┌─────────────┐                           │   │
│                 │ Add to      │                           │   │
│                 │ History     │                           │   │
│                 └─────────────┘                           │   │
│                        │                                  │   │
│                        ▼                                  ▼   │
│                 ┌─────────────┐                    ┌─────────┐│
│                 │ Continue    │                    │  END    ││
│                 │  Loop       │                    │         ││
│                 └─────────────┘                    └─────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Formato de Respuesta del Agente

```json
{
    "thought": "Razonamiento interno del agente",
    "action": "execute|analyze|explain|ask|complete",
    "command": "nmap -sV target",
    "explanation": "Descripción de la acción",
    "findings": ["Hallazgo 1", "Hallazgo 2"],
    "recommendations": ["Recomendación 1"]
}
```

---

## 🗄️ Base de Datos

### Modelos (SQLModel)

```python
class ScanRecord(SQLModel):
    id: int
    target: str
    scan_type: str
    result: str
    project: str
    created_at: datetime

class AgentStep(SQLModel):
    id: int
    project: str
    objective: str
    step_number: int
    action_type: str
    thought: str
    command: str
    output: str
    explanation: str
    findings: str
    recommendations: str
    created_at: datetime
```

---

## ⚙️ Sistema de Configuración

### Prioridades

```
1. Variables de Entorno (.env)  ← Máxima prioridad
2. config.yaml                  ← Segunda prioridad
3. Valores por defecto          ← Si no hay nada más
```

### Implementación

```python
def get_config_value(yaml_path, env_var, default):
    # 1. Check environment variable
    if os.getenv(env_var):
        return os.getenv(env_var)
    
    # 2. Check YAML config
    if yaml_config.get(yaml_path):
        return yaml_config.get(yaml_path)
    
    # 3. Return default
    return default
```

---

## 🎨 Sistema de Display

### Temas

```python
@dataclass
class ColorTheme:
    name: str
    primary: str       # Headers
    secondary: str     # Borders
    accent: str        # Highlights
    success: str       # ✅
    error: str         # ❌
    warning: str       # ⚠️
    info: str          # ℹ️
```

### Modos

```python
class OutputMode(Enum):
    QUIET = "quiet"      # Solo errores
    NORMAL = "normal"    # Estándar
    VERBOSE = "verbose"  # Debug
```

---

## 📝 Sistema de Logging

```
┌─────────────────────────────────────────────┐
│                Logger                        │
│                                              │
│  ┌─────────────────┐  ┌─────────────────┐   │
│  │  File Handler   │  │ Console Handler │   │
│  │  (logs/*.log)   │  │ (stderr)        │   │
│  │                 │  │                 │   │
│  │ Level: DEBUG    │  │ Level: WARNING  │   │
│  │ Rotation: Daily │  │                 │   │
│  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🔄 Patrón de Retry (Tenacity)

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(Exception)
)
def chat_completion(messages, temperature, max_tokens):
    # API call with automatic retry
    pass
```

---

## 🐳 Docker

### Imagen Base
- `kalilinux/kali-rolling`
- Python 3 + pip
- Herramientas: nmap, gobuster, sqlmap, hydra, etc.

### Volúmenes
- `./logs:/app/logs`
- `./reports:/app/reports`
- `./database.db:/app/database.db`

### Network Mode
- `host` para escaneo de red local
- `bridge` para solo escaneos externos
