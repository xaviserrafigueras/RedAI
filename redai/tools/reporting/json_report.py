"""
JSON Report Generator for RedAI.
Exports scan results and agent steps in machine-readable JSON format.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from redai.core.display import display
from redai.core.logger import get_logger
from redai.database.repository import get_history, get_agent_steps

logger = get_logger("reporting.json")


def json_report(project: str, filename: str = None, auto: bool = False) -> Optional[str]:
    """
    Generate a JSON report for a project.
    
    Args:
        project: Project name
        filename: Output filename (default: {project}_report.json)
        auto: Auto-confirm without prompts
    
    Returns:
        Path to generated file, or None if failed
    """
    display.header(f"📊 JSON Report Generator: {project}")
    
    # Get data from database
    records = get_history(project)
    agent_steps = get_agent_steps(project)
    
    if not records and not agent_steps:
        display.warning(f"No records found for project: {project}")
        return None
    
    # Build report structure
    report = {
        "metadata": {
            "project": project,
            "generated_at": datetime.now().isoformat(),
            "generator": "RedAI",
            "version": "1.0.0"
        },
        "summary": {
            "total_scans": len(records),
            "total_steps": len(agent_steps),
            "objectives": len(set(step.objective for step in agent_steps)) if agent_steps else 0
        },
        "objectives": [],
        "scans": []
    }
    
    # Group agent steps by objective
    objectives_dict = {}
    for step in agent_steps:
        if step.objective not in objectives_dict:
            objectives_dict[step.objective] = {
                "name": step.objective,
                "steps": []
            }
        
        objectives_dict[step.objective]["steps"].append({
            "step_number": step.step_number,
            "action_type": step.action_type,
            "thought": step.thought,
            "command": step.command,
            "output": step.output[:2000] if step.output else None,  # Truncate large outputs
            "explanation": step.explanation,
            "findings": step.findings.split("\n") if step.findings else [],
            "recommendations": step.recommendations.split("\n") if step.recommendations else [],
            "timestamp": step.timestamp.isoformat() if step.timestamp else None
        })
    
    report["objectives"] = list(objectives_dict.values())
    
    # Add scan records
    for record in records:
        report["scans"].append({
            "target": record.target,
            "scan_type": record.scan_type,
            "result": record.result[:2000] if record.result else None,  # Truncate
            "timestamp": record.timestamp.isoformat() if record.timestamp else None
        })
    
    # Generate filename
    if not filename:
        filename = f"{project}_report.json"
    
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    output_path = reports_dir / filename
    
    # Write JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        display.success(f"JSON report saved to: {output_path}")
        logger.info(f"Generated JSON report: {output_path}")
        return str(output_path)
        
    except Exception as e:
        display.error(f"Failed to write JSON report: {e}")
        logger.error(f"JSON report error: {e}")
        return None


def get_report_data(project: str) -> dict:
    """
    Get report data as a dictionary (for API use).
    
    Args:
        project: Project name
    
    Returns:
        Report data dictionary
    """
    records = get_history(project)
    agent_steps = get_agent_steps(project)
    
    return {
        "project": project,
        "scans": len(records),
        "steps": len(agent_steps),
        "records": records,
        "agent_steps": agent_steps
    }
