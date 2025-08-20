import time
from pathlib import Path
from typing import Optional
from .core.rule_engine import RuleEngine
from .core.scanner import ComplianceScanner
from .core.downloader import RepositoryDownloader
from .services.ai_analyzer import AIAnalyzer
from .services.report_generator import ReportGenerator
from .models.repository import RepositoryInfo
from .models.compliance import ComplianceReport
from .utils.config import get_config


class ComplianceChecker:
    """Main orchestrator for repository compliance checking"""

    def __init__(self, rules_file: str | None = None):
        self.config = get_config()

        # Initialize components
        self.rule_engine = RuleEngine(rules_file or self.config["rules_file"])
        self.scanner = ComplianceScanner(self.rule_engine)
        self.downloader = RepositoryDownloader()
        self.ai_analyzer = AIAnalyzer()
        self.report_generator = ReportGenerator(self.config["output_dir"])

        # Validate setup
        if not self.rule_engine.get_rules():
            raise ValueError(
                "No compliance rules loaded. Please check your rules file."
            )

    def check_repository(self, repo_url: str) -> ComplianceReport:
        """Main method to check repository compliance"""
        start_time = time.time()

        print(f"Starting compliance check for: {repo_url}")

        try:
            # Step 1: Download repository
            repo_info = self.downloader.download_repository(repo_url)
            if not repo_info:
                raise Exception("Failed to download repository")

            # Step 2: Scan for violations
            violations = self.scanner.scan_repository(repo_info)

            # Step 3: Generate AI recommendations
            recommendations = self.ai_analyzer.generate_recommendations(violations)

            # Step 4: Generate comprehensive report
            scan_duration = time.time() - start_time
            report = self.report_generator.generate_report(
                repo_info, violations, recommendations, scan_duration
            )

            # Step 5: Display and save results
            self._handle_results(report, repo_info)

            return report

        except Exception as e:
            print(f"Error during compliance check: {e}")
            raise
        finally:
            # Clean up temporary files
            if "repo_info" in locals() and repo_info is not None:
                self.downloader.cleanup(repo_info)

    def _handle_results(self, report: ComplianceReport, repo_info: RepositoryInfo):
        """Handle the results of the compliance check"""
        # Print console report
        self.report_generator.print_console_report(report)

        # Save reports
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_filename = f"compliance_report_{repo_info.name}_{timestamp}"

        # Save JSON report
        json_file = self.report_generator.save_json_report(
            report, f"{base_filename}.json"
        )

        # Save Markdown report
        md_file = self.report_generator.save_markdown_report(
            report, f"{base_filename}.md"
        )

        print(f"\nReports saved:")
        print(f"  JSON: {json_file}")
        print(f"  Markdown: {md_file}")

    def get_compliance_summary(self, repo_url: str) -> dict:
        """Get a quick compliance summary without full report generation"""
        try:
            repo_info = self.downloader.download_repository(repo_url)
            if not repo_info:
                return {"error": "Failed to download repository"}

            violations = self.scanner.scan_repository(repo_info)

            summary = {
                "repository": repo_info.name,
                "url": repo_url,
                "total_violations": len(violations),
                "severity_breakdown": {},
                "top_violations": [],
            }

            # Count by severity
            for violation in violations:
                severity = violation.severity
                summary["severity_breakdown"][severity] = (
                    summary["severity_breakdown"].get(severity, 0) + 1
                )

            # Get top violations
            top_violations = sorted(violations, key=lambda x: x.severity, reverse=True)[
                :5
            ]
            summary["top_violations"] = [
                {
                    "rule_id": v.rule_id,
                    "title": v.rule_title,
                    "severity": v.severity,
                    "file": v.file_path,
                }
                for v in top_violations
            ]

            return summary

        except Exception as e:
            return {"error": str(e)}
        finally:
            if "repo_info" in locals() and repo_info is not None:
                self.downloader.cleanup(repo_info)

    def validate_rules(self) -> dict:
        """Validate all loaded compliance rules"""
        rules = self.rule_engine.get_rules()
        validation_results = {
            "total_rules": len(rules),
            "valid_rules": 0,
            "invalid_rules": 0,
            "errors": [],
        }

        for rule in rules:
            errors = self.rule_engine.validate_rule(rule)
            if errors:
                validation_results["invalid_rules"] += 1
                validation_results["errors"].append(
                    {"rule_id": rule.id, "errors": errors}
                )
            else:
                validation_results["valid_rules"] += 1

        return validation_results
