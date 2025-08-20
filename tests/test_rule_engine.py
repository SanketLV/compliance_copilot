import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ..src.core.rule_engine import RuleEngine
from ..src.models.compliance import ComplianceRule


class TestRuleEngine:
    """Test cases for RuleEngine class"""

    def test_load_rules(self):
        """Test loading rules from file"""
        # This test would require a mock rules file
        # For now, we'll test the basic structure
        engine = RuleEngine("config/rules.json")
        assert hasattr(engine, "rules")

    def test_rule_validation(self):
        """Test rule validation logic"""
        engine = RuleEngine("config/rules.json")

        # Test valid rule
        valid_rule = ComplianceRule(
            id="TEST001",
            title="Test Rule",
            description="Test description",
            file_patterns=["*.py"],
            regex_patterns=["test.*pattern"],
            severity="high",
            compliance_mapping=["TEST"],
            fix_suggestion="Fix this",
        )

        errors = engine.validate_rule(valid_rule)
        assert len(errors) == 0

        # Test invalid rule
        invalid_rule = ComplianceRule(
            id="",
            title="",
            description="Test description",
            file_patterns=["*.py"],
            regex_patterns=["test.*pattern"],
            severity="invalid",
            compliance_mapping=["TEST"],
            fix_suggestion="Fix this",
        )

        errors = engine.validate_rule(invalid_rule)
        assert len(errors) > 0
        assert any("Rule ID is required" in error for error in errors)
        assert any("Invalid severity level" in error for error in errors)

    def test_file_pattern_matching(self):
        """Test file pattern matching logic"""
        engine = RuleEngine("config/rules.json")

        rule = ComplianceRule(
            id="TEST001",
            title="Test Rule",
            description="Test description",
            file_patterns=["*.py", "test.py", "**/config/*"],
            regex_patterns=[],
            severity="medium",
            compliance_mapping=["TEST"],
            fix_suggestion="Fix this",
        )

        # Test wildcard patterns
        assert engine.match_file_pattern(Path("file.py"), rule)
        assert engine.match_file_pattern(Path("test.py"), rule)
        assert engine.match_file_pattern(Path("src/config/settings.py"), rule)
        assert not engine.match_file_pattern(Path("file.js"), rule)
