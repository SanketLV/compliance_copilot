import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from ..models.compliance import ComplianceReport, ComplianceViolation
from ..models.repository import RepositoryInfo


class ReportGenerator:
    """Generates comprehensive compliance reports in various formats"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_report(
        self,
        repo_info: RepositoryInfo,
        violations: List[ComplianceViolation],
        recommendations: List[str],
        scan_duration: float,
    ) -> ComplianceReport:
        """Generate a comprehensive compliance report"""

        # Count violations by severity
        severity_counts = self._count_violations_by_severity(violations)

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(violations)

        # Create report
        report = ComplianceReport(
            repository_url=repo_info.url,
            repository_name=repo_info.name,
            scan_timestamp=datetime.now().isoformat(),
            total_violations=len(violations),
            high_severity=severity_counts.get("high", 0),
            medium_severity=severity_counts.get("medium", 0),
            low_severity=severity_counts.get("low", 0),
            critical_severity=severity_counts.get("critical", 0),
            violations=violations,
            compliance_score=compliance_score,
            recommendations=recommendations,
            scan_duration=scan_duration,
        )

        return report

    def _count_violations_by_severity(
        self, violations: List[ComplianceViolation]
    ) -> Dict[str, int]:
        """Count violations grouped by severity"""
        counts = {}
        for violation in violations:
            counts[violation.severity] = counts.get(violation.severity, 0) + 1
        return counts

    def _calculate_compliance_score(
        self, violations: List[ComplianceViolation]
    ) -> float:
        """Calculate overall compliance score (0-100)"""
        if not violations:
            return 100.0

        # Weight violations by severity
        severity_weights = {"low": 1, "medium": 2, "high": 3, "critical": 5}
        total_weight = 0

        for violation in violations:
            weight = severity_weights.get(violation.severity, 1)
            total_weight += weight

        # Calculate score (higher violations = lower score)
        # Assume worst case: all rules violated with high severity
        max_possible_violations = 50  # Reasonable upper bound
        score = max(0, 100 - (total_weight / max_possible_violations) * 100)

        return round(score, 1)

    def save_json_report(
        self, report: ComplianceReport, filename: str | None = None
    ) -> str:
        """Save report as JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compliance_report_{report.repository_name}_{timestamp}.json"

        filepath = self.output_dir / filename

        # Convert dataclass to dict for JSON serialization
        report_dict = self._report_to_dict(report)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)

        print(f"JSON report saved to: {filepath}")
        return str(filepath)

    def save_markdown_report(
        self, report: ComplianceReport, filename: str | None = None
    ) -> str:
        """Save report as Markdown file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compliance_report_{report.repository_name}_{timestamp}.md"

        filepath = self.output_dir / filename

        markdown_content = self._generate_markdown_content(report)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Markdown report saved to: {filepath}")
        return str(filepath)

    def _report_to_dict(self, report: ComplianceReport) -> Dict[str, Any]:
        """Convert ComplianceReport to dictionary for JSON serialization"""
        return {
            "repository_url": report.repository_url,
            "repository_name": report.repository_name,
            "scan_timestamp": report.scan_timestamp,
            "total_violations": report.total_violations,
            "high_severity": report.high_severity,
            "medium_severity": report.medium_severity,
            "low_severity": report.low_severity,
            "critical_severity": report.critical_severity,
            "compliance_score": report.compliance_score,
            "scan_duration": report.scan_duration,
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "rule_title": v.rule_title,
                    "severity": v.severity,
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "content": v.content,
                    "description": v.description,
                    "compliance_mapping": v.compliance_mapping,
                    "fix_suggestion": v.fix_suggestion,
                    "context": v.context,
                }
                for v in report.violations
            ],
            "recommendations": report.recommendations,
        }

    def _generate_markdown_content(self, report: ComplianceReport) -> str:
        """Generate Markdown content for the report"""
        content = []

        # Header
        content.append(f"# Compliance Report: {report.repository_name}")
        content.append("")
        content.append(f"**Repository:** {report.repository_url}")
        content.append(f"**Scan Date:** {report.scan_timestamp}")
        content.append(f"**Scan Duration:** {report.scan_duration:.2f} seconds")
        content.append("")

        # Summary
        content.append("## Executive Summary")
        content.append("")
        content.append(f"**Compliance Score:** {report.compliance_score}/100")
        content.append(f"**Total Violations:** {report.total_violations}")
        content.append(f"**High Severity:** {report.high_severity}")
        content.append(f"**Medium Severity:** {report.medium_severity}")
        content.append(f"**Low Severity:** {report.low_severity}")
        content.append(f"**Critical Severity:** {report.critical_severity}")
        content.append("")

        # Violations
        if report.violations:
            content.append("## Violations Details")
            content.append("")

            for violation in report.violations:
                content.append(f"### {violation.rule_id}: {violation.rule_title}")
                content.append("")
                content.append(f"**Severity:** {violation.severity}")
                content.append(f"**File:** `{violation.file_path}`")
                if violation.line_number > 0:
                    content.append(f"**Line:** {violation.line_number}")
                content.append(f"**Description:** {violation.description}")
                content.append(
                    f"**Compliance:** {', '.join(violation.compliance_mapping)}"
                )
                content.append("")
                content.append("**Content:**")
                content.append(f"```")
                content.append(violation.content)
                content.append(f"```")
                content.append("")
                content.append("**Fix Suggestion:**")
                content.append(f"{violation.fix_suggestion}")
                content.append("")
                content.append("---")
                content.append("")

        # Recommendations
        if report.recommendations:
            content.append("## Recommendations")
            content.append("")
            for i, rec in enumerate(report.recommendations, 1):
                content.append(f"{i}. {rec}")
            content.append("")

        return "\n".join(content)

    def print_console_report(self, report: ComplianceReport):
        """Print formatted report to console"""
        print("\n" + "=" * 80)
        print("REPOSITORY COMPLIANCE REPORT")
        print("=" * 80)
        print(f"Repository: {report.repository_name}")
        print(f"URL: {report.repository_url}")
        print(f"Scan Date: {report.scan_timestamp}")
        print(f"Compliance Score: {report.compliance_score}/100")
        print(f"Total Violations: {report.total_violations}")
        print(f"High Severity: {report.high_severity}")
        print(f"Medium Severity: {report.medium_severity}")
        print(f"Low Severity: {report.low_severity}")
        print(f"Critical Severity: {report.critical_severity}")
        print(f"Scan Duration: {report.scan_duration:.2f} seconds")

        if report.violations:
            print("\nVIOLATIONS DETAILS:")
            print("-" * 80)
            for violation in report.violations:
                print(f"\nRule {violation.rule_id}: {violation.rule_title}")
                print(f"Severity: {violation.severity}")
                print(f"File: {violation.file_path}")
                if violation.line_number > 0:
                    print(f"Line: {violation.line_number}")
                print(f"Content: {violation.content}")
                print(f"Description: {violation.description}")
                print(f"Compliance: {', '.join(violation.compliance_mapping)}")
                print(f"Fix: {violation.fix_suggestion}")

        if report.recommendations:
            print("\nRECOMMENDATIONS:")
            print("-" * 80)
            for i, rec in enumerate(report.recommendations, 1):
                print(f"{i}. {rec}")

        print("\n" + "=" * 80)
