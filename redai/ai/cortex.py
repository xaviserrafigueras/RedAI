"""
Cortex Memory System for AI Agent.
Provides persistent memory and context management for autonomous operations.
"""

import json
from typing import Dict, Any
from datetime import datetime


class CortexMemory:
    """
    Memoria Persistente para el Agente (Knowledge Graph Simplificado).
    Guarda 'Hechos' (Facts) sobre el objetivo.
    """
    
    def __init__(self):
        self.memory = {
            "objective": "",       # Meta Principal del Usuario
            "targets": {},         # IP/Host -> Detalles
            "findings": [],        # Vulnerabilidades/Hallazgos encontrados
            "executed_tools": [],  # Registro de herramientas usadas para no repetir
            "step_history": []     # HISTORIAL PROFUNDO DE ACCIONES
        }

    def set_objective(self, objective: str):
        self.memory["objective"] = objective

    def update_target(self, target: str, data: Dict):
        """Actualiza información sobre un target (ej: puertos, servicio)."""
        if target not in self.memory["targets"]:
            self.memory["targets"][target] = {}
        self.memory["targets"][target].update(data)

    def add_finding(self, finding: str):
        if finding not in self.memory["findings"]:
            self.memory["findings"].append(finding)

    def record_step(self, thought: str, action: str, output: str):
        """Registra un paso completo en la narrativa de la misión."""
        step = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "thought": thought,
            "action": action,
            "output_summary": output[:500] + "..." if len(output) > 500 else output
        }
        self.memory["step_history"].append(step)

    def record_action(self, tool_name: str, params: str):
        self.memory["executed_tools"].append(f"{tool_name}({params})")

    def get_context_json(self) -> str:
        """Devuelve la memoria actual como JSON string para el System Prompt."""
        return json.dumps(self.memory, indent=2)
    
    def get_history_text(self) -> str:
        """Genera un resumen de los últimos pasos."""
        history = self.memory.get("step_history", [])
        if not history:
            return "No details yet."
        
        txt = ""
        for i, h in enumerate(history[-8:]):  # Últimos 8 pasos
            txt += f"Step {i+1} [{h['timestamp']}]: {h['action']} -> {h['output_summary']}\n"
        return txt

    def clear(self):
        self.memory = {
            "objective": "",
            "targets": {},
            "findings": [],
            "executed_tools": [],
            "step_history": []
        }


class RedAICortex:
    """
    Cerebro Central que coordina Memoria y Planificación.
    """
    
    def __init__(self, internal_tools: Dict[str, str]):
        self.memory = CortexMemory()
        self.internal_tools = internal_tools  # Diccionario {nombre: descripcion}

    def generated_system_prompt(self) -> str:
        """Genera el System Prompt Dinámico con la memoria actual."""
        
        prompt = f"""
Eres RedAI Cortex, un Sistema de Hacking Autónomo Avanzado.
NO eres un asistente de chat. Eres un OPERADOR DE CIBERSEGURIDAD en un entorno Kali Linux.

TUS HERRAMIENTAS (System Tools):
Tienes acceso total a la terminal mediante 'bash'.
- Recon: nmap, masscan, whatweb, dig, whois...
- Web: sqlmap, gobuster, nikto, wpscan...
- Network: aircrack-ng, wash, hping3...
- General: curl, python3, grep, cat, ssh...

IMPORTANTE:
El usuario tiene instaladas MUCHAS herramientas personalizadas (Nuclei, Subfinder, Feroxbuster, scripts propios, etc.).
NO te limites a las herramientas por defecto.
Si crees que una herramienta específica es mejor para la tarea, verifica si está instalada (`which herramienta`) y ÚSALA.

ACCIONES DISPONIBLES:
- bash: Ejecutar comandos de sistema NATIVOS.
- install: Instalar dependencias o herramientas (apt, pip, git). Usa esto si falta algo.

TU MEMORIA ACTUAL (Estado del Pentest):
{self.memory.get_context_json()}

HISTORIAL RECIENTE (LO QUE HAS HECHO):
{self.memory.get_history_text()}

TU MISIÓN:
1. Analizar el OBJETIVO actual.
2. Consultar tu HISTORIAL. ¿Qué acabas de hacer? ¿Cómo salió?
3. PLANIFICAR el siguiente paso lógico.
4. EJECUTAR herramienta vía 'bash'.

REGLAS:
- NO alucines resultados. Si necesitas saber algo, ESCANEA.
- Tienes acceso a herramientas internas (ej: 'wifi_stealer', 'nmap'). ÚSALAS.
- MANTÉN LA MEMORIA VIVA: Si un comando (nmap/scan) devuelve IPs o Puertos, DEBES emitir un "memory_update" en tu JSON inmediatamente.
- NO esperes al final. Registra cada hallazgo al momento.

FORMATO DE RESPUESTA (IMPORTANTE):
Debes responder SIEMPRE con un bloque JSON para tomar acciones o pensar:

```json
{{
  "thought": "Pensamiento racional sobre qué hacer.",
  "action": "tool_name",
  "params": "argumentos",
  "memory_update": {{ "target": "IP", "data": {{ "port": 80 }} }}  <-- Opcional, para guardar info nueva
}}
```

Si solo quieres hablar con el usuario o pedir confirmación:
```json
{{
  "thought": "Necesito pregutar al usuario...",
  "action": "talk",
  "params": "Mensaje para el usuario"
}}
```
"""
        return prompt.strip()
