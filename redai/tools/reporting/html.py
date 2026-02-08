"""
HTML Report Generator - Enhanced version with objectives and steps
"""

import os
import json
from datetime import datetime
from collections import defaultdict

from rich.console import Console

from redai.core.display import display
from redai.database.repository import get_history, get_agent_steps


console = Console()


def html_report(project: str, filename: str = "report.html", auto: bool = False):
    """Genera reporte HTML interactivo con objetivos y pasos detallados."""
    display.header(f"HTML Report Generator: {project}")
    
    records = get_history(project)
    agent_steps = get_agent_steps(project)
    
    if not records and not agent_steps:
        display.warning(f"No records found for project: {project}")
        return
    
    # Group agent steps by objective
    objectives = defaultdict(list)
    for step in agent_steps:
        objectives[step.objective].append(step)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RedAI Report - {project}</title>
    <style>
        :root {{
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-step: #1a1a24;
            --text-primary: #e4e4e7;
            --text-secondary: #a1a1aa;
            --accent-red: #ef4444;
            --accent-green: #22c55e;
            --accent-blue: #3b82f6;
            --accent-purple: #a855f7;
            --accent-yellow: #eab308;
            --accent-cyan: #06b6d4;
            --border: #27272a;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 40px 20px;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        /* Header */
        .header {{
            text-align: center;
            padding: 60px 0;
            background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(168,85,247,0.1));
            border-radius: 20px;
            margin-bottom: 40px;
            border: 1px solid var(--border);
        }}
        .header h1 {{
            font-size: 3em;
            background: linear-gradient(135deg, var(--accent-red), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .header .project-name {{ color: var(--accent-cyan); font-size: 1.2em; }}
        .header .timestamp {{ color: var(--text-secondary); font-size: 0.9em; margin-top: 15px; }}
        
        /* Stats Grid */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }}
        .stat-card {{
            background: var(--bg-card);
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-2px); border-color: var(--accent-purple); }}
        .stat-card h3 {{ font-size: 2.5em; color: var(--accent-blue); margin-bottom: 5px; }}
        .stat-card p {{ color: var(--text-secondary); }}
        
        /* Objective Section */
        .objective {{
            background: var(--bg-card);
            border-radius: 20px;
            margin-bottom: 30px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        .objective-header {{
            background: linear-gradient(90deg, rgba(239,68,68,0.2), transparent);
            padding: 25px 30px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .objective-header .icon {{ font-size: 1.5em; }}
        .objective-header h2 {{ color: var(--text-primary); font-size: 1.3em; flex: 1; }}
        .objective-header .badge {{
            background: var(--accent-purple);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        
        /* Steps */
        .steps {{ padding: 20px 30px; }}
        
        .step {{
            background: var(--bg-step);
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        .step:last-child {{ margin-bottom: 0; }}
        
        .step-header {{
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
        }}
        .step-header:hover {{ background: rgba(255,255,255,0.02); }}
        
        .step-number {{
            background: var(--accent-blue);
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .step-type {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .step-type.execute {{ background: var(--accent-green); color: #000; }}
        .step-type.analyze {{ background: var(--accent-purple); color: #fff; }}
        .step-type.explain {{ background: var(--accent-cyan); color: #000; }}
        .step-type.complete {{ background: var(--accent-yellow); color: #000; }}
        .step-type.ask {{ background: var(--accent-blue); color: #fff; }}
        
        .step-time {{ color: var(--text-secondary); font-size: 0.8em; margin-left: auto; }}
        
        .step-content {{ padding: 20px; }}
        
        /* Thought Box */
        .thought {{
            background: rgba(59,130,246,0.1);
            border-left: 3px solid var(--accent-blue);
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 0 8px 8px 0;
        }}
        .thought-label {{ color: var(--accent-blue); font-size: 0.8em; margin-bottom: 5px; font-weight: 600; }}
        
        /* Command Box */
        .command {{
            background: #1e1e2e;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        .command-header {{
            background: #2a2a3e;
            padding: 10px 15px;
            color: var(--accent-green);
            font-size: 0.8em;
            font-weight: 600;
        }}
        .command pre {{
            padding: 15px;
            margin: 0;
            overflow-x: auto;
            font-family: 'Fira Code', 'Monaco', monospace;
            font-size: 0.9em;
            color: var(--accent-green);
        }}
        
        /* Output Box */
        .output {{
            background: #0d0d12;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
            max-height: 400px;
            overflow-y: auto;
        }}
        .output-header {{
            background: #1a1a24;
            padding: 10px 15px;
            color: var(--accent-yellow);
            font-size: 0.8em;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        .output pre {{
            padding: 15px;
            margin: 0;
            overflow-x: auto;
            font-family: 'Fira Code', 'Monaco', monospace;
            font-size: 0.8em;
            white-space: pre-wrap;
            word-break: break-all;
        }}
        
        /* Findings/Recommendations */
        .findings, .recommendations {{
            background: rgba(34,197,94,0.1);
            border-radius: 8px;
            padding: 15px 20px;
            margin-top: 15px;
        }}
        .findings {{ border-left: 3px solid var(--accent-green); }}
        .recommendations {{ border-left: 3px solid var(--accent-yellow); background: rgba(234,179,8,0.1); }}
        .findings-label, .recommendations-label {{
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .findings-label {{ color: var(--accent-green); }}
        .recommendations-label {{ color: var(--accent-yellow); }}
        .findings ul, .recommendations ul {{ margin-left: 20px; }}
        .findings li, .recommendations li {{ margin-bottom: 5px; }}
        
        /* Legacy Scans Section */
        .legacy-section {{ margin-top: 50px; }}
        .legacy-section h2 {{
            color: var(--text-secondary);
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
        }}
        
        .scan-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        .scan-header {{
            background: var(--bg-step);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .scan-type {{ color: var(--accent-green); font-weight: bold; }}
        .scan-target {{ color: var(--accent-blue); }}
        .scan-body {{ padding: 15px 20px; }}
        .scan-body pre {{
            background: #0d0d12;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.85em;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 0;
            color: var(--text-secondary);
            font-size: 0.85em;
            border-top: 1px solid var(--border);
            margin-top: 50px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 RedAI Security Report</h1>
            <p class="project-name">Project: <strong>{project}</strong></p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(objectives)}</h3>
                <p>Objectives</p>
            </div>
            <div class="stat-card">
                <h3>{len(agent_steps)}</h3>
                <p>Agent Steps</p>
            </div>
            <div class="stat-card">
                <h3>{len(records)}</h3>
                <p>Total Scans</p>
            </div>
            <div class="stat-card">
                <h3>{len(set(r.target for r in records))}</h3>
                <p>Unique Targets</p>
            </div>
        </div>
"""
    
    # Add objectives with steps
    if objectives:
        html += "<h2 style='color: var(--text-primary); margin-bottom: 20px;'>🎯 Objectives & Steps</h2>\n"
        
        for obj_text, steps in objectives.items():
            html += f"""
        <div class="objective">
            <div class="objective-header">
                <span class="icon">🎯</span>
                <h2>{escape_html(obj_text[:200])}</h2>
                <span class="badge">{len(steps)} steps</span>
            </div>
            <div class="steps">
"""
            for step in steps:
                html += generate_step_html(step)
            
            html += """
            </div>
        </div>
"""
    
    # Legacy scans (non-agent)
    non_agent_records = [r for r in records if r.command_type != "cortex_agent"]
    if non_agent_records:
        html += """
        <div class="legacy-section">
            <h2>📋 Other Scan Results</h2>
"""
        for record in non_agent_records[:20]:  # Limit to last 20
            output_escaped = escape_html(record.output[:5000])
            html += f"""
            <div class="scan-card">
                <div class="scan-header">
                    <span class="scan-type">{record.command_type.upper()}</span>
                    <span class="scan-target">{escape_html(record.target)}</span>
                    <span style="color: var(--text-secondary); font-size: 0.85em;">
                        {record.timestamp.strftime('%Y-%m-%d %H:%M')}
                    </span>
                </div>
                <div class="scan-body">
                    <pre>{output_escaped}</pre>
                </div>
            </div>
"""
        html += "</div>"
    
    html += """
        <div class="footer">
        <p>Generated by <a href="https://github.com/xaviserrafigueras/RedAI" style="color: var(--accent-cyan);">RedAI</a> - Autonomous Pentesting Framework</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save file in reports/project folder
    from pathlib import Path
    try:
        reports_dir = Path("reports") / project
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = reports_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        display.success(f"Report saved: {output_path.absolute()}")
        display.info("Open in browser to view.")
        
    except Exception as e:
        display.error(f"Failed to save report: {e}")


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def generate_step_html(step) -> str:
    """Generate HTML for a single agent step."""
    html = f"""
                <div class="step">
                    <div class="step-header">
                        <span class="step-number">{step.step_number}</span>
                        <span class="step-type {step.action_type}">{step.action_type}</span>
                        <span class="step-time">{step.timestamp.strftime('%H:%M:%S')}</span>
                    </div>
                    <div class="step-content">
"""
    
    # Thought
    if step.thought:
        html += f"""
                        <div class="thought">
                            <div class="thought-label">💭 AI THOUGHT</div>
                            <p>{escape_html(step.thought)}</p>
                        </div>
"""
    
    # Command
    if step.command:
        html += f"""
                        <div class="command">
                            <div class="command-header">⚡ COMMAND</div>
                            <pre>{escape_html(step.command)}</pre>
                        </div>
"""
    
    # Output
    if step.output:
        html += f"""
                        <div class="output">
                            <div class="output-header">📤 OUTPUT</div>
                            <pre>{escape_html(step.output[:8000])}</pre>
                        </div>
"""
    
    # Explanation
    if step.explanation:
        html += f"""
                        <div class="thought" style="border-color: var(--accent-cyan); background: rgba(6,182,212,0.1);">
                            <div class="thought-label" style="color: var(--accent-cyan);">📝 EXPLANATION</div>
                            <p>{escape_html(step.explanation)}</p>
                        </div>
"""
    
    # Findings
    if step.findings:
        try:
            findings_list = json.loads(step.findings)
            if findings_list:
                html += """
                        <div class="findings">
                            <div class="findings-label">🔍 FINDINGS</div>
                            <ul>
"""
                for f in findings_list:
                    html += f"                                <li>{escape_html(f)}</li>\n"
                html += """
                            </ul>
                        </div>
"""
        except:
            pass
    
    # Recommendations
    if step.recommendations:
        try:
            rec_list = json.loads(step.recommendations)
            if rec_list:
                html += """
                        <div class="recommendations">
                            <div class="recommendations-label">💡 RECOMMENDATIONS</div>
                            <ul>
"""
                for r in rec_list:
                    html += f"                                <li>{escape_html(r)}</li>\n"
                html += """
                            </ul>
                        </div>
"""
        except:
            pass
    
    html += """
                    </div>
                </div>
"""
    return html
