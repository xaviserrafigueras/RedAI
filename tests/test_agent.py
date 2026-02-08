"""
Tests for the RedAI Agent module.
Tests parsing of AI responses and action handling.
"""

import pytest
from redai.tools.agent import parse_ai_response


class TestParseAiResponse:
    """Tests for the parse_ai_response function."""
    
    def test_parse_execute_action_in_code_block(self, sample_ai_response_execute):
        """Test parsing execute action from code block."""
        result = parse_ai_response(sample_ai_response_execute)
        
        assert result is not None
        assert result["action"] == "execute"
        assert result["command"] == "nmap -sV 192.168.1.1"
        assert "thought" in result
    
    def test_parse_analyze_action_direct_json(self, sample_ai_response_analyze):
        """Test parsing analyze action from direct JSON."""
        result = parse_ai_response(sample_ai_response_analyze)
        
        assert result is not None
        assert result["action"] == "analyze"
        assert isinstance(result["findings"], list)
        assert len(result["findings"]) == 2
    
    def test_parse_complete_action(self, sample_ai_response_complete):
        """Test parsing complete action."""
        result = parse_ai_response(sample_ai_response_complete)
        
        assert result is not None
        assert result["action"] == "complete"
        assert "summary" in result
        assert "recommendations" in result
    
    def test_parse_explain_action(self, sample_ai_response_explain):
        """Test parsing explain action."""
        result = parse_ai_response(sample_ai_response_explain)
        
        assert result is not None
        assert result["action"] == "explain"
        assert "title" in result
        assert "explanation" in result
        assert isinstance(result.get("commands"), list)
    
    def test_parse_invalid_json_returns_none(self, invalid_json_response):
        """Test that invalid JSON returns None."""
        result = parse_ai_response(invalid_json_response)
        
        assert result is None
    
    def test_parse_empty_string_returns_none(self):
        """Test that empty string returns None."""
        result = parse_ai_response("")
        
        assert result is None
    
    def test_parse_json_with_extra_text(self):
        """Test parsing JSON with surrounding text."""
        response = '''Here is my analysis:
        ```json
        {"action": "execute", "command": "whoami"}
        ```
        Let me know if you need more info.'''
        
        result = parse_ai_response(response)
        
        assert result is not None
        assert result["action"] == "execute"
        assert result["command"] == "whoami"


class TestAgentActions:
    """Tests for agent action validation."""
    
    def test_valid_actions(self):
        """Test that valid actions are recognized."""
        valid_actions = ["execute", "analyze", "explain", "complete", "ask"]
        
        for action in valid_actions:
            response = f'{{"action": "{action}", "thought": "test"}}'
            result = parse_ai_response(response)
            assert result is not None
            assert result["action"] == action
    
    def test_execute_requires_command(self):
        """Test that execute action should have command field."""
        response = '{"action": "execute", "command": "ls -la"}'
        result = parse_ai_response(response)
        
        assert result is not None
        assert "command" in result
