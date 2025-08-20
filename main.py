"""
Repository Compliance Copilot - Main Entry Point
A comprehensive tool for checking repository compliance against security and governance rules.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.compliance_checker import ComplianceChecker
from src.utils.config import load_env


def main():
    """Main entry point for the compliance checker"""
    # Load environment variables
    load_env()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Repository Compliance Copilot - Check repository compliance against security rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python main.py                                    # Interactive mode
            python main.py -u https://github.com/user/repo   # Check specific repository
            python main.py --summary -u https://github.com/user/repo  # Quick summary only
            python main.py --validate-rules                  # Validate compliance rules
            python main.py --help                            # Show this help message
        """,
    )

    parser.add_argument(
        "-u", "--url", type=str, help="Repository URL to check (GitHub/GitLab)"
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Generate quick summary only (no detailed report)",
    )

    parser.add_argument(
        "--validate-rules",
        action="store_true",
        help="Validate all compliance rules and exit",
    )

    parser.add_argument(
        "--rules-file",
        type=str,
        help="Path to custom rules file (default: config/rules.json)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for reports (default: reports/)",
    )

    args = parser.parse_args()

    try:
        # Initialize compliance checker
        checker = ComplianceChecker(rules_file=args.rules_file)

        # Handle different modes
        if args.validate_rules:
            print("Validating compliance rules...")
            validation_results = checker.validate_rules()

            print(f"\nValidation Results:")
            print(f"Total Rules: {validation_results['total_rules']}")
            print(f"Valid Rules: {validation_results['valid_rules']}")
            print(f"Invalid Rules: {validation_results['invalid_rules']}")

            if validation_results["errors"]:
                print(f"\nValidation Errors:")
                for error in validation_results["errors"]:
                    print(f"  Rule {error['rule_id']}:")
                    for err in error["errors"]:
                        print(f"    - {err}")

            return

        # Get repository URL
        repo_url = args.url
        if not repo_url:
            repo_url = input("\nEnter repository URL (GitHub/GitLab): ").strip()

        if not repo_url:
            print("No repository URL provided. Exiting.")
            return

        # Check compliance
        if args.summary:
            print(f"Generating compliance summary for: {repo_url}")
            summary = checker.get_compliance_summary(repo_url)

            if "error" in summary:
                print(f"Error: {summary['error']}")
                return

            print(f"\nCompliance Summary for {summary['repository']}:")
            print(f"Total Violations: {summary['total_violations']}")
            print(f"Severity Breakdown: {summary['severity_breakdown']}")

            if summary["top_violations"]:
                print("\nTop Violations:")
                for i, violation in enumerate(summary["top_violations"], 1):
                    print(
                        f"  {i}. {violation['rule_id']}: {violation['title']} ({violation['severity']})"
                    )
                    print(f"     File: {violation['file']}")
        else:
            print(f"Running full compliance check for: {repo_url}")
            report = checker.check_repository(repo_url)

            print(f"\nCompliance check completed successfully!")
            print(f"Repository: {report.repository_name}")
            print(f"Compliance Score: {report.compliance_score}/100")
            print(f"Total Violations: {report.total_violations}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
