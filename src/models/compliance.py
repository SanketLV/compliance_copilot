from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ComplianceRule:
    """
    Represents a compliance rule with patterns and metadata
    """

    id: str
    title: str
    description: str
    file_patterns: List[str]
    regex_patterns: List[str]
    severity: str
    compliance_mapping: List[str]
    fix_suggestion: str

    def __post_init__(self):
        """validate rule data after initialization"""
        if not self.id or not self.title:
            raise ValueError("Rule ID and title are required")
        if self.severity not in ["low", "medium", "high", "critical"]:
            raise ValueError("Severity must be low, medium, high, or critical")


# @dataclass
# class ComplianceViolation:
