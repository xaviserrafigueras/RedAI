"""
Base utilities for security tools.
Common decorators and helper functions.
"""

from functools import wraps
from typing import Callable, Any

from redai.database.repository import save_scan
from redai.core.utils import suggest_ai_analysis
from redai.core.display import display


def save_and_analyze(
    target: str,
    command_type: str,
    output: str,
    project: str,
    context: str,
    auto: bool = False
):
    """
    Common pattern for tools: save to DB and offer AI analysis.
    
    Args:
        target: The scan target (IP, domain, etc.)
        command_type: Type of command/tool used
        output: Tool output to save
        project: Project name for organization
        context: Context description for AI analysis
        auto: If True, skip AI analysis prompt
    """
    save_scan(target, command_type, output, project)
    
    if not auto:
        suggest_ai_analysis(output, context)


def tool_command(tool_key: str):
    """
    Decorator for tool commands that adds common functionality.
    - Shows tool info at start
    - Handles exceptions gracefully
    
    Args:
        tool_key: Key for TOOL_DESCRIPTIONS lookup
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                display.tool_info(tool_key)
                return func(*args, **kwargs)
            except Exception as e:
                display.error(f"Error in {func.__name__}: {e}")
                return None
        return wrapper
    return decorator
