import os
from pathlib import Path
from typing import List, Set
from ..models.compliance import ComplianceRule, ComplianceViolation
from ..models.repository import RepositoryInfo
from .rule_engine import RuleEngine


class ComplianceScanner:
    """Scans repository files for compliance violations"""

    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine
        self.excluded_dirs = {
            ".git",
            "node_modules",
            "venv",
            "__pycache__",
            ".pytest_cache",
            "build",
            "dist",
        }
        self.excluded_files = {".DS_Store", "Thumbs.db"}

    def scan_repository(self, repo_info: RepositoryInfo) -> List[ComplianceViolation]:
        """Scan entire repository for compliance violations"""
        print(f"Scanning repository: {repo_info.name}")

        all_violations = []
        scanned_files = 0

        for file_path in self._get_files_to_scan(repo_info.local_path):
            scanned_files += 1
            violations = self._scan_file(file_path, repo_info)
            all_violations.extend(violations)

        print(f"Scanned {scanned_files} files, found {len(all_violations)} violations")
        return all_violations

    def _get_files_to_scan(self, repo_path: Path) -> List[Path]:
        """Get list of files to scan, excluding certain directories and files"""
        files_to_scan = []

        for root, dirs, files in os.walk(repo_path):
            # Filter out excluded directories
            dirs[:] = [
                d for d in dirs if d not in self.excluded_dirs and not d.startswith(".")
            ]

            for file in files:
                if file not in self.excluded_files and not file.startswith("."):
                    file_path = Path(root) / file
                    files_to_scan.append(file_path)

        return files_to_scan

    def _scan_file(
        self, file_path: Path, repo_info: RepositoryInfo
    ) -> List[ComplianceViolation]:
        """Scan a single file for compliance violations"""
        violations = []

        try:
            # check each rule against the file
            for rule in self.rule_engine.get_rules():
                rule_violations = self._check_rule_against_file(
                    file_path, rule, repo_info
                )
                violations.extend(rule_violations)
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")

        return violations

    def _check_rule_against_file(
        self, file_path: Path, rule: ComplianceRule, repo_info: RepositoryInfo
    ) -> List[ComplianceViolation]:
        """Check if a specific rule is violated by a file"""
        violations = []

        # Check if file matches the rule's file patterns
        if not self.rule_engine.match_file_pattern(file_path, rule):
            return violations

        try:
            # Read file content
            content = self._read_file_content(file_path)
            if content is None:
                return violations

            # Check regex patterns
            regex_matches = self.rule_engine.match_regex_patterns(content, rule)

            for match in regex_matches:
                violation = ComplianceViolation(
                    rule_id=rule.id,
                    rule_title=rule.title,
                    severity=rule.severity,
                    file_path=repo_info.get_relative_path(file_path),
                    line_number=match["line_number"],
                    content=match["content"],
                    description=rule.description,
                    compliance_mapping=rule.compliance_mapping,
                    fix_suggestion=rule.fix_suggestion,
                    context=match.get("match", ""),
                )
                violations.append(violation)

            # For rules without regex patterns, check if file exists
            if not rule.regex_patterns and rule.file_patterns:
                if self.rule_engine.match_file_pattern(file_path, rule):
                    violation = ComplianceViolation(
                        rule_id=rule.id,
                        rule_title=rule.title,
                        severity=rule.severity,
                        file_path=repo_info.get_relative_path(file_path),
                        line_number=0,
                        content="File found",
                        description=rule.description,
                        compliance_mapping=rule.compliance_mapping,
                        fix_suggestion=rule.fix_suggestion,
                    )
                    violations.append(violation)

        except Exception as e:
            print(f"Error checking rule {rule.id} against file {file_path}: {e}")

        return violations

    def _read_file_content(self, file_path: Path) -> str | None:
        """Read file content with proper encoding handling"""
        try:
            # Try UTF-8 first
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fall back to latin-1 for binary-like files
                with open(file_path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception:
                # Skip files that can't be read as text
                return None
        except Exception:
            return None

    def add_excluded_directory(self, dir_name: str) -> None:
        """Add a directory to the exclusion list"""
        self.excluded_dirs.add(dir_name)

    def add_excluded_files(self, file_name: str) -> None:
        """Add a file to the exclusion list"""
        self.excluded_files.add(file_name)
