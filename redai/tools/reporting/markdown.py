"""
Markdown Report Generator for RedAI.
Exports scan results and agent steps in readable Markdown format.
Perfect for documentation, GitHub, and generating PDFs.
"""

from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Optional

from redai.core.display import display
from redai.core.logger import get_logger
from redai.database.repository import get_history, get_agent_steps

logger = get_logger("reporting.markdown")


def markdown_report(project: str, filename: str = None, auto: bool = False) -> Optional[str]:
    """
    Generate a Markdown report for a project.
    
    Args:
        project: Project name
        filename: Output filename (default: {project}_report.md)
        auto: Auto-confirm without prompts
    
    Returns:
        Path to generated file, or None if failed
    """
    display.header(f"📝 Markdown Report Generator: {project}")
    
    # Get data from database
    records = get_history(project)
    agent_steps = get_agent_steps(project)
    
    if not records and not agent_steps:
        display.warning(f"No records found for project: {project}")
        return None
    
    # Group agent steps by objective
    objectives = defaultdict(list)
    for step in agent_steps:
        objectives[step.objective].append(step)
    
    # Build Markdown content
    md_lines = []
    
    # Header
    md_lines.append(f"# 🔴 RedAI Report: {project}")
    md_lines.append("")
    md_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append("")
    
    # Summary
    md_lines.append("## 📊 Summary")
    md_lines.append("")
    md_lines.append(f"| Metric | Value |")
    md_lines.append(f"|--------|-------|")
    md_lines.append(f"| Total Objectives | {len(objectives)} |")
    md_lines.append(f"| Total Steps | {len(agent_steps)} |")
    md_lines.append(f"| Total Scans | {len(records)} |")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Objectives and Steps
    if objectives:
        md_lines.append("## 🎯 Objectives")
        md_lines.append("")
        
        for idx, (objective, steps) in enumerate(objectives.items(), 1):
            md_lines.append(f"### {idx}. {objective}")
            md_lines.append("")
            
            for step in sorted(steps, key=lambda x: x.step_number):
                action_emoji = {
                    "execute": "⚡",
                    "analyze": "🔍",
                    "explain": "💡",
                    "complete": "✅",
                    "ask": "❓"
                }.get(step.action_type, "📌")
                
                md_lines.append(f"#### {action_emoji} Step {step.step_number}: {step.action_type.title()}")
                md_lines.append("")
                
                # Thought
                if step.thought:
                    md_lines.append(f"**Thought:** {step.thought}")
                    md_lines.append("")
                
                # Command
                if step.command:
                    md_lines.append(f"**Command:**")
                    md_lines.append(f"```bash")
                    md_lines.append(step.command)
                    md_lines.append(f"```")
                    md_lines.append("")
                
                # Output (truncated)
                if step.output:
                    output = step.output[:1000]
                    if len(step.output) > 1000:
                        output += "\n... (truncated)"
                    md_lines.append(f"**Output:**")
                    md_lines.append(f"```")
                    md_lines.append(output)
                    md_lines.append(f"```")
                    md_lines.append("")
                
                # Explanation
                if step.explanation:
                    md_lines.append(f"**Explanation:** {step.explanation}")
                    md_lines.append("")
                
                # Findings
                if step.findings:
                    md_lines.append(f"**Findings:**")
                    for finding in step.findings.split("\n"):
                        if finding.strip():
                            md_lines.append(f"- {finding.strip()}")
                    md_lines.append("")
                
                # Recommendations
                if step.recommendations:
                    md_lines.append(f"**Recommendations:**")
                    for rec in step.recommendations.split("\n"):
                        if rec.strip():
                            md_lines.append(f"- {rec.strip()}")
                    md_lines.append("")
            
            md_lines.append("---")
            md_lines.append("")
    
    # Legacy Scans
    if records:
        md_lines.append("## 📋 Scan Results")
        md_lines.append("")
        md_lines.append("| Target | Type | Timestamp |")
        md_lines.append("|--------|------|-----------|")
        
        for record in records[:20]:  # Limit to 20
            timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M') if record.timestamp else "N/A"
            md_lines.append(f"| `{record.target}` | {record.command_type} | {timestamp} |")
        
        if len(records) > 20:
            md_lines.append(f"| ... | *{len(records) - 20} more* | ... |")
        
        md_lines.append("")
    
    # Footer
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*Report generated by [RedAI](https://github.com/xaviserrafigueras/RedAI) - Autonomous AI Pentesting Framework*")
    
    # Generate filename
    if not filename:
        filename = f"{project}_report.md"
    
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    output_path = reports_dir / filename
    
    # Write Markdown file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        
        display.success(f"Markdown report saved to: {output_path}")
        logger.info(f"Generated Markdown report: {output_path}")
        return str(output_path)
        
    except Exception as e:
        display.error(f"Failed to write Markdown report: {e}")
        logger.error(f"Markdown report error: {e}")
        return None
