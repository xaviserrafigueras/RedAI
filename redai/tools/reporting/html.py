"""
HTML Report Generator
"""

import os
from datetime import datetime

from rich.console import Console

from redai.core.display import display
from redai.database.repository import get_history


console = Console()


def html_report(project: str, filename: str = "report.html", auto: bool = False):
    """Genera reporte HTML interactivo con gráficos y tablas."""
    display.header(f"HTML Report Generator: {project}")
    
    records = get_history(project)
    
    if not records:
        display.warning(f"No records found for project: {project}")
        return
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RedAI Report - {project}</title>
    <style>
        :root {{
            --bg-dark: #0d1117;
            --bg-card: #161b22;
            --text-primary: #c9d1d9;
            --accent-red: #f85149;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
        }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #30363d;
        }}
        .header h1 {{
            color: var(--accent-red);
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #30363d;
        }}
        .stat-card h3 {{
            color: var(--accent-blue);
            font-size: 2em;
            margin: 0;
        }}
        .scan-card {{
            background: var(--bg-card);
            border: 1px solid #30363d;
            border-radius: 10px;
            margin: 20px 0;
            overflow: hidden;
        }}
        .scan-header {{
            background: #21262d;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .scan-type {{
            color: var(--accent-green);
            font-weight: bold;
        }}
        .scan-target {{
            color: var(--accent-blue);
        }}
        .scan-body {{
            padding: 20px;
        }}
        pre {{
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.85em;
            max-height: 400px;
            overflow-y: auto;
        }}
        .timestamp {{
            color: #8b949e;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 RedAI Security Report</h1>
            <p>Project: <strong>{project}</strong></p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(records)}</h3>
                <p>Total Scans</p>
            </div>
            <div class="stat-card">
                <h3>{len(set(r.command_type for r in records))}</h3>
                <p>Tool Types</p>
            </div>
            <div class="stat-card">
                <h3>{len(set(r.target for r in records))}</h3>
                <p>Unique Targets</p>
            </div>
        </div>
        
        <h2>📋 Scan Results</h2>
"""
    
    for record in records:
        output_escaped = record.output.replace('<', '&lt;').replace('>', '&gt;')
        html += f"""
        <div class="scan-card">
            <div class="scan-header">
                <span class="scan-type">{record.command_type.upper()}</span>
                <span class="scan-target">{record.target}</span>
                <span class="timestamp">{record.timestamp.strftime('%Y-%m-%d %H:%M')}</span>
            </div>
            <div class="scan-body">
                <pre>{output_escaped[:5000]}</pre>
            </div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>"""
    
    # Save file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        display.success(f"Report saved: {os.path.abspath(filename)}")
        display.info("Open in browser to view.")
        
    except Exception as e:
        display.error(f"Failed to save report: {e}")
