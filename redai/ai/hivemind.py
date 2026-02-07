"""
HiveMind Multi-Agent System.
Coordinates specialized AI agents for different pentesting tasks.
"""

import re
from typing import Dict

from redai.ai.client import get_client, get_model_name


class AgentRole:
    """Represents a specialized agent role with its personality and capabilities."""
    
    def __init__(self, name: str, icon: str, color: str, system_prompt: str):
        self.name = name
        self.icon = icon
        self.color = color
        self.system_prompt = system_prompt


# Definición de Roles Especializados
ROLES: Dict[str, AgentRole] = {
    "MANAGER": AgentRole(
        "Manager", "👑", "magenta",
        "Eres el LÍDER de un Red Team (RedAI). Tu trabajo es COORDINAR. "
        "NO ejecutas comandos técnicos complejos tú mismo. "
        "Tu misión:\n"
        "1. Analizar la petición del usuario.\n"
        "2. Decidir qué especialista debe actuar.\n"
        "3. DELEGAR usando el formato: 'DELEGATE_TO: [ROLE_NAME] Reason: [Instrucción]'.\n"
        "Roles disponibles:\n"
        "- RECON: Para escaneos (nmap, shodan, subdominios), descubrir servicios y puertos.\n"
        "- EXPLOIT: Para atacar (sqlmap, xss, exploits, fuerza bruta) una vez detectada una vulnerabilidad.\n"
        "- GENERAL: Para responder dudas generales o charlar.\n"
        "\nSi el usuario pide algo complejo, divídelo. Primero RECON, luego analizas, luego EXPLOIT."
    ),
    "RECON": AgentRole(
        "Recon", "🔭", "cyan",
        "Eres el especialista en RECONOCIMIENTO e INTELIGENCIA. "
        "Tu único objetivo es ENUMERAR y DESCUBRIR.\n"
        "Herramientas Clave: nmap, shodan_scan, subdomains, fuzz, wp_scan.\n"
        "FORMATO EJECUCIÓN: Usa ```execute\ncomando\n``` para lanzar herramientas.\n"
        "Se preciso y técnico. Reporta puertos abiertos, versiones y directorios."
    ),
    "EXPLOIT": AgentRole(
        "Exploit", "💥", "red",
        "Eres el especialista en ATAQUE y EXPLOTACIÓN. "
        "Tu objetivo es COMPROMETER el sistema basándote en el reconocimiento.\n"
        "Herramientas Clave: sqli, xss, search_exploits, payload_gen, crack, brute.\n"
        "FORMATO EJECUCIÓN: Usa ```execute\ncomando\n```.\n"
        "Nunca asumas vulnerabilidades. Verifica primero."
    )
}


class HiveMind:
    """
    Multi-agent coordinator that manages role-based AI specialists.
    """
    
    def __init__(self, project_name: str):
        self.project = project_name
        self.current_role = "MANAGER"
        self.history = []
        self.max_history = 15

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def think(self, user_input: str) -> dict:
        """Procesa el input usando el rol actual o cambiando según decida el Manager."""
        
        client = get_client()
        if not client:
            return {
                "role_name": "System",
                "role_icon": "❌",
                "role_color": "red",
                "content": "Error: No AI client configured."
            }
        
        target_role = ROLES.get(self.current_role, ROLES["MANAGER"])
        
        messages = [{"role": "system", "content": target_role.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": f"[User Input]: {user_input}"})

        try:
            response = client.chat.completions.create(
                model=get_model_name(),
                messages=messages,
                temperature=0.7
            )
            response_text = response.choices[0].message.content
            
            # Análisis de Delegación
            if "DELEGATE_TO:" in response_text:
                match = re.search(r"DELEGATE_TO:\s*(\w+)", response_text)
                if match:
                    new_role_key = match.group(1).upper()
                    if new_role_key in ROLES:
                        self.current_role = new_role_key
                        instruction = response_text.split("Reason:", 1)[1].strip() if "Reason:" in response_text else "Proceed."
                        self.add_message("system", f"Role switched to {new_role_key}. Instruction: {instruction}")
                        return self.think(f"Status update: I have taken control. Goal: {instruction}")
            
            self.add_message("assistant", response_text)
            
            return {
                "role_name": target_role.name,
                "role_icon": target_role.icon,
                "role_color": target_role.color,
                "content": response_text
            }

        except Exception as e:
            return {
                "role_name": "System",
                "role_icon": "❌",
                "role_color": "red",
                "content": f"Error thinking: {e}"
            }


# Global Hive Instance Cache
ACTIVE_HIVES: Dict[str, HiveMind] = {}


def get_hive(project: str) -> HiveMind:
    """Get or create a HiveMind instance for a project."""
    if project not in ACTIVE_HIVES:
        ACTIVE_HIVES[project] = HiveMind(project)
    return ACTIVE_HIVES[project]
