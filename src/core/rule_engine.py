import json
import re
from pathlib import Path
from typing import List, Dict, Any
from ..models.compliance import ComplianceRule


class RuleEngine:
    """manages compliance rules and rule matching logic"""

    def __init__(self, rules_file: str = "config/rules.json"):
        self.rules_file = rules_file
        self.rules: List[ComplianceRule] = []
        self._load_rules()

    def _load_rules(self):
        """Load compliance rules from JSON file"""
        try:
            with open(self.rules_file, "r", encoding="utf-8") as f:
                rules_data = json.load(f)

            self.rules = []
            for rule_data in rules_data:
                rule = ComplianceRule(
                    id=rule_data["id"],
                    title=rule_data["title"],
                    description=rule_data["description"],
                    file_patterns=rule_data["file_patterns"],
                    regex_patterns=rule_data["regex_patterns"],
                    severity=rule_data["severity"],
                    compliance_mapping=rule_data["compliance_mapping"],
                    fix_suggestion=rule_data["fix_suggestion"],
                )
                self.rules.append(rule)

            print(f"Loaded {len(self.rules)} compliance rules from {self.rules_file}")

        except FileNotFoundError:
            print(f"Rules file not found: {self.rules_file}")
            self.rules = []
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in rules file: {e}")
            self.rules = []
        except Exception as e:
            print(f"Error loading rules: {e}")
            self.rules = []

    def get_rules(self) -> List[ComplianceRule]:
        """Get all loaded rules"""
        return self.rules.copy()

    def get_rules_by_id(self, rule_id: str) -> ComplianceRule:
        """Get a specific rule by ID"""
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        raise ValueError(f"Rule with ID {rule_id} not found")

    def get_rules_by_severity(self, severity: str) -> List[ComplianceRule]:
        """Get rules filtered by severity level"""
        return [rule for rule in self.rules if rule.severity == severity]

    def match_file_pattern(self, file_path: Path, rule: ComplianceRule) -> bool:
        """Check if file matches any of the rule's file patterns"""
        file_path_str = str(file_path)

        for pattern in rule.file_patterns:
            if pattern.startswith("*"):
                # Handle wildcard patterns
                if file_path_str.endswith(pattern[1:]):
                    return True
            elif pattern.startswith("**/"):
                # Handle recursive directory patterns
                if pattern[3:] in file_path_str:
                    return True
            elif pattern in file_path_str:
                return True
            elif file_path.name == pattern:
                return True

        return False

    def match_regex_patterns(
        self, content: str, rule: ComplianceRule
    ) -> List[Dict[str, Any]]:
        """Check content against regex patterns and return matches"""
        matches = []
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            for pattern in rule.regex_patterns:
                try:
                    matches_found = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches_found:
                        matches.append(
                            {
                                "line_number": line_num,
                                "content": line.strip(),
                                "match": match.group(),
                                "start_pos": match.start(),
                                "end_pos": match.end(),
                            }
                        )
                except re.error as e:
                    print(f"Invalid regex pattern {pattern}: {e}")

        return matches

    def validate_rule(self, rule: ComplianceRule) -> List[str]:
        """Validate a rule and return any calidation errors"""
        errors = []

        if not rule.id:
            errors.append("Rule ID is required")
        if not rule.title:
            errors.append("Rule title is required")
        if rule.severity not in ["low", "medium", "high", "critical"]:
            errors.append("Invalid severity level")
        # Validate regex patterns
        for pattern in rule.regex_patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                errors.append(f"Invalid regex pattern '{pattern}': {e}")

        return errors
