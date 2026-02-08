"""
Pytest configuration and fixtures for RedAI tests.
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_ai_response_execute():
    """Sample AI response for execute action."""
    return '''```json
{
    "thought": "I need to scan the target to find open ports",
    "action": "execute",
    "command": "nmap -sV 192.168.1.1",
    "explanation": "Running service version detection scan"
}
```'''


@pytest.fixture
def sample_ai_response_analyze():
    """Sample AI response for analyze action."""
    return '''{
    "thought": "The scan shows interesting results",
    "action": "analyze",
    "findings": ["Port 22 SSH open", "Port 80 HTTP open"],
    "next_step": "Check for web vulnerabilities"
}'''


@pytest.fixture
def sample_ai_response_complete():
    """Sample AI response for complete action."""
    return '''{
    "thought": "I have completed the objective",
    "action": "complete",
    "summary": "Found 2 open ports with potential vulnerabilities",
    "recommendations": ["Update SSH", "Check web app for SQLi"]
}'''


@pytest.fixture
def sample_ai_response_explain():
    """Sample AI response for explain action."""
    return '''{
    "thought": "The user is asking how to perform a scan",
    "action": "explain",
    "title": "How to scan with nmap",
    "explanation": "Nmap is a network scanner...",
    "commands": ["nmap -sV target", "nmap -sC target"]
}'''


@pytest.fixture
def invalid_json_response():
    """Invalid JSON response."""
    return "This is not valid JSON at all"


@pytest.fixture
def temp_database(tmp_path):
    """Create a temporary database for testing."""
    db_path = tmp_path / "test_database.db"
    return str(db_path)
