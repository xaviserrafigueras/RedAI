"""
Tests for the RedAI Utils module.
Tests utility functions like tool installation checks.
"""

import pytest
import shutil
from unittest.mock import patch, MagicMock

from redai.core.utils import ensure_tool_installed, run_cli_tool


class TestEnsureToolInstalled:
    """Tests for the ensure_tool_installed function."""
    
    def test_tool_already_installed(self):
        """Test that function returns True for installed tools."""
        # 'python' should be installed on any system running these tests
        with patch('shutil.which', return_value='/usr/bin/python'):
            result = ensure_tool_installed("python")
            assert result is True
    
    def test_tool_not_installed_user_declines(self):
        """Test that function returns False when user declines installation."""
        with patch('shutil.which', return_value=None):
            with patch('rich.prompt.Confirm.ask', return_value=False):
                result = ensure_tool_installed("nonexistent_tool")
                assert result is False
    
    def test_tool_not_installed_installation_succeeds(self):
        """Test successful installation when user accepts."""
        with patch('shutil.which', return_value=None):
            with patch('rich.prompt.Confirm.ask', return_value=True):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)
                    result = ensure_tool_installed("some_tool")
                    assert result is True
    
    def test_tool_not_installed_installation_fails(self):
        """Test failed installation."""
        with patch('shutil.which', return_value=None):
            with patch('rich.prompt.Confirm.ask', return_value=True):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=1, stderr="Error")
                    result = ensure_tool_installed("failing_tool")
                    assert result is False


class TestRunCliTool:
    """Tests for the run_cli_tool function."""
    
    def test_run_installed_tool_success(self):
        """Test running a tool that is installed successfully."""
        with patch('redai.core.utils.ensure_tool_installed', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(
                    stdout="Success output",
                    stderr="",
                    returncode=0
                )
                success, output = run_cli_tool("echo", ["hello"])
                
                assert success is True
                assert "Success output" in output
    
    def test_run_tool_not_available(self):
        """Test running a tool that is not available."""
        with patch('redai.core.utils.ensure_tool_installed', return_value=False):
            success, output = run_cli_tool("nonexistent", ["arg"])
            
            assert success is False
            assert "no está disponible" in output


class TestInputValidation:
    """Tests for input validation utilities."""
    
    def test_valid_ip_address(self):
        """Test validation of IP addresses."""
        import re
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        
        valid_ips = ["192.168.1.1", "10.0.0.1", "255.255.255.255"]
        for ip in valid_ips:
            assert re.match(ip_pattern, ip) is not None
    
    def test_valid_domain(self):
        """Test validation of domain names."""
        import re
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        
        valid_domains = ["example.com", "sub.example.org", "test-site.co.uk"]
        for domain in valid_domains:
            assert re.match(domain_pattern, domain) is not None
    
    def test_invalid_targets(self):
        """Test that potentially dangerous inputs are caught."""
        dangerous_inputs = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& shutdown",
            "$(whoami)",
            "`id`"
        ]
        
        # These should NOT match valid target patterns
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        for dangerous in dangerous_inputs:
            import re
            assert re.match(ip_pattern, dangerous) is None
