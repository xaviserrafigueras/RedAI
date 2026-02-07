"""
Database repository functions for CRUD operations.
"""

from typing import Optional, List

from sqlmodel import SQLModel, create_engine, Session, select

from redai.database.models import ScanResult, AgentHistory


# Database configuration
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def init_db():
    """Initialize database and create tables."""
    SQLModel.metadata.create_all(engine)


def save_scan(
    target: str,
    command_type: str,
    output: str,
    project_name: str = "General",
    ai_analysis: Optional[str] = None
):
    """Save a scan result to the database."""
    with Session(engine) as session:
        scan = ScanResult(
            target=target,
            command_type=command_type,
            output=output,
            project_name=project_name,
            ai_analysis=ai_analysis
        )
        session.add(scan)
        session.commit()


def get_history(project_name: Optional[str] = None) -> List[ScanResult]:
    """Retrieve scan history, optionally filtered by project."""
    with Session(engine) as session:
        statement = select(ScanResult).order_by(ScanResult.timestamp.desc())
        if project_name:
            statement = statement.where(ScanResult.project_name == project_name)
        return session.exec(statement).all()


def get_projects() -> List[str]:
    """Get list of unique project names."""
    with Session(engine) as session:
        statement = select(ScanResult.project_name).distinct()
        return session.exec(statement).all()


# --- AGENT HISTORY FUNCTIONS ---

def save_agent_msg(project_name: str, role: str, content: str):
    """Save an agent chat message."""
    with Session(engine) as session:
        msg = AgentHistory(project_name=project_name, role=role, content=content)
        session.add(msg)
        session.commit()


def get_agent_history(project_name: str) -> List[AgentHistory]:
    """Retrieve agent chat history for a project."""
    with Session(engine) as session:
        statement = (
            select(AgentHistory)
            .where(AgentHistory.project_name == project_name)
            .order_by(AgentHistory.timestamp.asc())
        )
        return session.exec(statement).all()


# --- AGENT STEP FUNCTIONS (for detailed reports) ---

def save_agent_step(
    project_name: str,
    objective: str,
    step_number: int,
    action_type: str,
    thought: str = None,
    command: str = None,
    output: str = None,
    explanation: str = None,
    findings: str = None,
    recommendations: str = None
):
    """Save an agent step for detailed reporting."""
    from redai.database.models import AgentStep
    with Session(engine) as session:
        step = AgentStep(
            project_name=project_name,
            objective=objective,
            step_number=step_number,
            action_type=action_type,
            thought=thought,
            command=command,
            output=output,
            explanation=explanation,
            findings=findings,
            recommendations=recommendations
        )
        session.add(step)
        session.commit()


def get_agent_steps(project_name: str) -> List:
    """Retrieve all agent steps for a project, ordered by timestamp."""
    from redai.database.models import AgentStep
    with Session(engine) as session:
        statement = (
            select(AgentStep)
            .where(AgentStep.project_name == project_name)
            .order_by(AgentStep.timestamp.asc())
        )
        return session.exec(statement).all()

