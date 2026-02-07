"""
Database models using SQLModel.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class ScanResult(SQLModel, table=True):
    """Stores results from security scans and tool outputs."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    project_name: str = Field(default="General", index=True)
    target: str
    command_type: str
    output: str
    ai_analysis: Optional[str] = None


class AgentHistory(SQLModel, table=True):
    """Stores chat history for the AI agent."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    project_name: str = Field(index=True)
    role: str  # user, assistant, system
    content: str
