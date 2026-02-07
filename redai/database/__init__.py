"""
Database module - Models and repository functions
"""

from redai.database.models import ScanResult, AgentHistory
from redai.database.repository import (
    init_db,
    save_scan,
    get_history,
    get_projects,
    save_agent_msg,
    get_agent_history,
    engine
)
