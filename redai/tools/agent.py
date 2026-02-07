"""
RedAI Autonomous Agent - Cortex-powered AI pentesting
Step-by-step execution: Think → Execute → Analyze → Repeat
"""

import subprocess
import re
import json
from typing import Optional, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from redai.core.display import display
from redai.ai.client import get_client, get_model_name
from redai.ai.cortex import CortexMemory
from redai.database.repository import save_scan


console = Console()


AGENT_SYSTEM_PROMPT = """Eres RedAI Cortex, un Agente Autónomo de Pentesting.
Operas en Kali Linux con acceso completo a herramientas de seguridad.

IMPORTANTE: Cada OBJETIVO es independiente. Cuando el usuario introduce un nuevo objetivo,
enfócate SOLO en ese nuevo objetivo. No mezcles con objetivos anteriores.

MODO DE OPERACIÓN:
1. Analiza el objetivo del usuario
2. Si es una PREGUNTA (cómo, qué, por qué), responde con action="explain"
3. Si requiere EJECUCIÓN, planifica y ejecuta comandos
4. Analiza resultados y decide siguiente paso

HERRAMIENTAS DISPONIBLES:
- Recon: nmap, masscan, whois, dig, whatweb, nikto
- Web: sqlmap, gobuster, dirb, wpscan, nuclei
- OSINT: theHarvester, sublist3r, amass
- Exploit: searchsploit, msfconsole, hydra
- Network: arp-scan, netdiscover, tcpdump

FORMATO DE RESPUESTA (OBLIGATORIO - siempre JSON válido):

Para EXPLICAR o responder preguntas (cuando el usuario pregunta "cómo", "qué", "por qué"):
```json
{
    "thought": "El usuario pregunta cómo hacer X...",
    "action": "explain",
    "title": "Título de la explicación",
    "explanation": "Explicación detallada paso a paso...",
    "commands": ["comando1 opcional", "comando2 opcional"]
}
```

Para ejecutar un comando:
```json
{
    "thought": "Mi razonamiento sobre qué hacer...",
    "action": "execute",
    "command": "nmap -sV -sC target",
    "explanation": "Breve explicación del comando"
}
```

Para analizar resultados:
```json
{
    "thought": "Mi análisis del resultado...",
    "action": "analyze",
    "findings": ["Hallazgo 1", "Hallazgo 2"],
    "next_step": "Lo que haré a continuación"
}
```

Para pedir información al usuario:
```json
{
    "thought": "Necesito más información...",
    "action": "ask",
    "question": "¿Cuál es el scope autorizado?"
}
```

Para finalizar:
```json
{
    "thought": "He completado el objetivo...",
    "action": "complete",
    "summary": "Resumen de hallazgos",
    "recommendations": ["Recomendación 1", "Recomendación 2"]
}
```

REGLAS:
- Si el usuario hace una PREGUNTA, usa action="explain" para responder directamente
- Solo UN comando por respuesta cuando uses action="execute"
- Siempre responde en JSON válido
- No inventes resultados, ejecuta comandos reales
- Cada nuevo objetivo es INDEPENDIENTE del anterior
"""


def parse_ai_response(response_text: str) -> Optional[Dict[str, Any]]:
    """Extrae JSON de la respuesta de la IA."""
    # Try to find JSON in code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to parse entire response as JSON
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Try to find any JSON object
    json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


def execute_command(cmd: str, timeout: int = 120) -> str:
    """Ejecuta un comando en bash y devuelve el output."""
    import signal
    import os
    
    try:
        # Use Popen for better control
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            output = stdout + stderr
            return output if output else "(No output)"
        except subprocess.TimeoutExpired:
            # Kill entire process group
            try:
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                else:
                    process.kill()
            except:
                pass
            process.wait()
            
            # Reset terminal state
            try:
                os.system('stty sane 2>/dev/null')
            except:
                pass
            
            return f"(Command timed out after {timeout}s - process killed)"
            
    except Exception as e:
        return f"(Error: {e})"


def agent(project: str = "General", auto_approve: bool = False):
    """RedAI Cortex - Agente autónomo de pentesting con IA."""
    display.header("🧠 RedAI Cortex", "Autonomous Penetration Testing Agent")
    
    console.print(Panel(
        "[bold cyan]Welcome to RedAI Cortex[/bold cyan]\n\n"
        "I'm an AI-powered pentesting agent that operates step-by-step:\n"
        "• [cyan]THINK[/cyan] → Analyze and plan\n"
        "• [green]EXECUTE[/green] → Run security tools\n"
        "• [yellow]ANALYZE[/yellow] → Interpret results\n"
        "• [magenta]REPEAT[/magenta] → Continue until complete\n\n"
        "[yellow]⚠️ Use only on authorized systems![/yellow]",
        border_style="red"
    ))
    
    client = get_client()
    if not client:
        display.error("No AI client configured. Check your .env file.")
        return
    
    memory = CortexMemory()
    conversation = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    
    # Session memory - persists across objectives
    session_summary = []  # List of key findings/recommendations from this session
    
    console.print("\n[bold green]Agent Ready.[/bold green]")
    console.print("[dim]Enter your objective. Type 'exit' to quit.[/dim]\n")
    
    while True:
        try:
            # Get user input
            try:
                user_input = input("\n🔴 Objective: ")
            except EOFError:
                break
            
            if not user_input.strip():
                continue
            
            if user_input.lower() == 'exit':
                console.print("[red]Shutting down Cortex...[/red]")
                break
            
            # Set objective in memory
            memory.set_objective(user_input)
            
            # Reset conversation but inject session context
            conversation = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
            
            # Include session summary if we have previous findings
            if session_summary:
                context = "CONTEXTO DE SESIÓN (hallazgos y recomendaciones previas):\n"
                context += "\n".join([f"- {s}" for s in session_summary[-10:]])  # Keep last 10 items
                context += f"\n\nNUEVO OBJETIVO: {user_input}"
                conversation.append({"role": "user", "content": context})
            else:
                conversation.append({"role": "user", "content": f"NUEVO OBJETIVO: {user_input}"})
            
            # Autonomous loop
            step = 0
            while step < 20:  # Max 20 steps to prevent infinite loops
                step += 1
                
                # Step 1: THINK - Get AI response
                console.print(f"\n[bold cyan]═══ STEP {step}: THINKING ═══[/bold cyan]")
                
                with console.status("[bold yellow]AI is thinking...[/bold yellow]"):
                    response = client.chat.completions.create(
                        model=get_model_name(),
                        messages=conversation,
                        temperature=0.7
                    )
                    ai_text = response.choices[0].message.content
                
                # Parse JSON response
                parsed = parse_ai_response(ai_text)
                
                if not parsed:
                    console.print(Panel(ai_text, title="🧠 AI Response", border_style="magenta"))
                    console.print("[yellow]Could not parse structured response. Showing raw output.[/yellow]")
                    break
                
                # Show thought
                thought = parsed.get("thought", "")
                if thought:
                    console.print(Panel(thought, title="💭 Thought", border_style="blue"))
                
                action = parsed.get("action", "")
                
                # Step 2: EXECUTE
                if action == "execute":
                    cmd = parsed.get("command", "")
                    explanation = parsed.get("explanation", "")
                    
                    console.print(f"\n[bold green]═══ STEP {step}: EXECUTE ═══[/bold green]")
                    console.print(Panel(
                        Syntax(cmd, "bash", theme="monokai"),
                        title="⚡ Command",
                        border_style="green"
                    ))
                    if explanation:
                        console.print(f"[dim]{explanation}[/dim]")
                    
                    # Confirm execution
                    if not auto_approve:
                        try:
                            confirm = input("\n Execute this command? [Y/n]: ").strip().lower()
                        except EOFError:
                            confirm = "y"
                        
                        if confirm == "n":
                            console.print("[yellow]Skipped. Tell me what to do instead.[/yellow]")
                            try:
                                user_feedback = input(" Your input: ")
                            except EOFError:
                                user_feedback = "skip"
                            conversation.append({"role": "user", "content": f"Usuario decidió no ejecutar. Feedback: {user_feedback}"})
                            continue
                    
                    # Execute
                    console.print("\n[bold yellow]═══ OUTPUT ═══[/bold yellow]")
                    output = execute_command(cmd)
                    
                    # Show output (truncated if too long)
                    display_output = output[:3000] + "\n...(truncated)" if len(output) > 3000 else output
                    console.print(Panel(display_output, title="📤 Result", border_style="yellow"))
                    
                    # Record in memory
                    memory.record_step(thought, cmd, output)
                    
                    # Save scan info to session summary (for context in future objectives)
                    if "nmap" in cmd.lower() or "scan" in cmd.lower():
                        session_summary.append(f"[ESCANEO] Ejecutado: {cmd[:80]}")
                    
                    # Save to DB
                    save_scan(
                        target=user_input[:50],
                        command_type="cortex_agent",
                        output=output[:5000],
                        project_name=project
                    )
                    
                    # Add to conversation for next iteration
                    conversation.append({"role": "assistant", "content": ai_text})
                    conversation.append({"role": "user", "content": f"RESULTADO DEL COMANDO:\n{output[:4000]}\n\nAnaliza este resultado y decide el siguiente paso."})
                
                # Step 3: ANALYZE
                elif action == "analyze":
                    findings = parsed.get("findings", [])
                    next_step = parsed.get("next_step", "")
                    
                    console.print(f"\n[bold magenta]═══ ANALYSIS ═══[/bold magenta]")
                    
                    if findings:
                        findings_text = "\n".join([f"• {f}" for f in findings])
                        console.print(Panel(findings_text, title="🔍 Findings", border_style="magenta"))
                        # Save findings to session memory
                        for f in findings:
                            session_summary.append(f"[HALLAZGO] {f}")
                    
                    if next_step:
                        console.print(Panel(next_step, title="➡️ Next Step", border_style="cyan"))
                    
                    conversation.append({"role": "assistant", "content": ai_text})
                    conversation.append({"role": "user", "content": "Procede con el siguiente paso."})
                
                # ASK user
                elif action == "ask":
                    question = parsed.get("question", "")
                    console.print(Panel(question, title="❓ Agent Question", border_style="cyan"))
                    
                    try:
                        answer = input(" Your answer: ")
                    except EOFError:
                        answer = "skip"
                    conversation.append({"role": "assistant", "content": ai_text})
                    conversation.append({"role": "user", "content": f"RESPUESTA: {answer}"})
                
                # EXPLAIN - Direct explanation without command execution
                elif action == "explain":
                    title = parsed.get("title", "Explicación")
                    explanation = parsed.get("explanation", "")
                    commands = parsed.get("commands", [])
                    
                    console.print(f"\n[bold cyan]═══ {title.upper()} ═══[/bold cyan]")
                    console.print(Panel(explanation, title="📚 Explicación", border_style="cyan"))
                    
                    if commands:
                        cmd_text = "\n".join([f"  {cmd}" for cmd in commands])
                        console.print(Panel(cmd_text, title="💻 Comandos Sugeridos", border_style="green"))
                        # Save suggested commands to session memory
                        session_summary.append(f"[RECOMENDACIÓN] {title}: " + ", ".join(commands[:3]))
                    
                    # End the loop for this objective - explanation is complete
                    break
                
                # COMPLETE
                elif action == "complete":
                    summary = parsed.get("summary", "")
                    recommendations = parsed.get("recommendations", [])
                    
                    console.print(f"\n[bold green]═══ MISSION COMPLETE ═══[/bold green]")
                    console.print(Panel(summary, title="📋 Summary", border_style="green"))
                    
                    if recommendations:
                        rec_text = "\n".join([f"• {r}" for r in recommendations])
                        console.print(Panel(rec_text, title="💡 Recommendations", border_style="yellow"))
                        # Save recommendations to session memory
                        for r in recommendations:
                            session_summary.append(f"[RECOMENDACIÓN] {r}")
                    
                    break
                
                else:
                    # Unknown action, show raw and break
                    console.print(Panel(ai_text, title="🧠 AI Response", border_style="magenta"))
                    break
            
            console.print("\n[dim]Enter a new objective or 'exit' to quit.[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit properly.[/yellow]")
        except Exception as e:
            display.error(f"Agent Error: {e}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
