"""
RedAI Autonomous Agent - Cortex-powered AI pentesting
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from redai.core.display import display
from redai.ai.cortex import RedAICortex
from redai.ai.hivemind import get_hive
from redai.config import TOOL_DESCRIPTIONS


console = Console()


def agent(project: str = "General", auto_approve: bool = False):
    """RedAI Cortex - Agente autónomo de pentesting con IA."""
    display.header("🧠 RedAI Cortex", "Autonomous Penetration Testing Agent")
    
    console.print(Panel(
        "[bold cyan]Welcome to RedAI Cortex[/bold cyan]\n\n"
        "I'm an AI-powered pentesting agent that can:\n"
        "• Analyze targets and plan attack strategies\n"
        "• Execute security tools autonomously\n"
        "• Adapt based on discovered vulnerabilities\n"
        "• Generate comprehensive reports\n\n"
        "[yellow]⚠️ Use only on authorized systems![/yellow]",
        border_style="red"
    ))
    
    # Initialize HiveMind
    hive = get_hive(project)
    
    # Initialize Cortex
    cortex = RedAICortex(internal_tools=TOOL_DESCRIPTIONS)
    
    console.print("\n[bold green]Agent Ready.[/bold green]")
    console.print("[dim]Type 'exit' to quit, 'status' to see progress, 'help' for commands.[/dim]\n")
    
    while True:
        try:
            user_input = Prompt.ask("[bold red]🔴 RedAI[/bold red]")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() == 'exit':
                console.print("[red]Shutting down Cortex...[/red]")
                break
                
            if user_input.lower() == 'status':
                status = cortex.get_status()
                console.print(Panel(status, title="Agent Status", border_style="cyan"))
                continue
                
            if user_input.lower() == 'help':
                console.print(Panel(
                    "[cyan]Commands:[/cyan]\n"
                    "• [green]scan <target>[/green] - Start reconnaissance\n"
                    "• [green]analyze <output>[/green] - AI analysis\n"
                    "• [green]exploit <vuln>[/green] - Suggest exploits\n"
                    "• [green]report[/green] - Generate findings report\n"
                    "• [green]status[/green] - Show current progress\n"
                    "• [green]exit[/green] - Quit agent",
                    title="Help",
                    border_style="green"
                ))
                continue
            
            # Process through HiveMind
            display.step("Thinking...")
            
            with console.status("[bold cyan]Consulting HiveMind...[/bold cyan]"):
                response = hive.think(user_input)
            
            # Display response
            if response:
                role = response.get("role_name", "MANAGER")
                content = response.get("content", "No response generated.")
                
                console.print(Panel(
                    content,
                    title=f"🧠 {role}",
                    border_style="magenta"
                ))
                
                # Check if action is suggested
                if "EXECUTE:" in content:
                    suggested_cmd = content.split("EXECUTE:")[1].split("\n")[0].strip()
                    
                    if auto_approve or Confirm.ask(f"Execute suggested command: [cyan]{suggested_cmd}[/cyan]?"):
                        display.step(f"Executing: {suggested_cmd}")
                        # Would execute the command here
                        console.print("[green]Command execution would happen here.[/green]")
                        
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit properly.[/yellow]")
        except Exception as e:
            display.error(f"Agent Error: {e}")


# Typer command wrapper
app = typer.Typer()

@app.command()
def run_agent(
    project: str = typer.Option("General", help="Project name"),
    auto: typer.Option = typer.Option(False, "--auto", help="Auto-approve commands")
):
    """Launch RedAI Autonomous Agent."""
    agent(project=project, auto_approve=auto)
