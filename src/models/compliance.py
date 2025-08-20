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


@dataclass
class ComplianceViolation:
    """
    Represents a specific compliance violation found in the repository
    """

    rule_id: str
    rule_title: str
    severity: str
    file_path: str
    line_number: int
    content: str
    description: str
    compliance_mapping: List[str]
    fix_suggestion: str
    context: Optional[str] = None

    def __post_init__(self):
        """Validate violation data after initialization"""
        if not self.rule_id or not self.file_path:
            raise ValueError("Rule ID and file path are required")


@dataclass
class ComplianceReport:
    """
    Comprehensive compliance report for a repository
    """

    repository_url: str
    repository_name: str
    scan_timestamp: str
    total_violations: int
    high_severity: int
    medium_severity: int
    low_severity: int
    critical_severity: int
    violations: List[ComplianceViolation]
    compliance_score: float
    recommendations: List[str]
    scan_duration: float

    def get_violations_by_severity(self, severity: str) -> List[ComplianceViolation]:
        """Get violations filtered by severity level"""
        return [v for v in self.violations if v.severity == severity]

    def get_violations_by_rule(self, rule_id: str) -> List[ComplianceViolation]:
        """Get violations filtered by rule ID"""
        return [v for v in self.violations if v.rule_id == rule_id]
