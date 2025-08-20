import os
from typing import List, Optional
from ..models.compliance import ComplianceViolation
from ..utils.config import get_config


class AIAnalyzer:
    """Provides AI-Powered analysis and recommendations using Portia/Google Gemini"""

    def __init__(self):
        self.config = get_config()
        self.portia = self._initialize_portia()

    def _initialize_portia(self):
        """Initialize Portia for AI analysis"""
        try:
            from portia import Config, LLMProvider, Portia, example_tool_registry

            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                print("Warning: GOOGLE_API_KEY not found. AI analysis will be limited.")
                return None

            google_config = Config.from_default(
                llm_provider=LLMProvider.GOOGLE,
                default_model="google/gemini-2.0-flash",
                google_api_key=google_api_key,
            )
            return Portia(config=google_config, tools=example_tool_registry)
        except ImportError:
            print("Warning: Portia not available. AI analysis will be limited.")
            return None
        except Exception as e:
            print(f"Error initializing Portia: {e}")
            return None

    def generate_recommendations(
        self, violations: List[ComplianceViolation]
    ) -> List[str]:
        """Generate AI-Powered recommendations based on violations"""
        if not self.portia:
            return self._generate_fallback_recommendations(violations)

        try:
            # Create a summary of violations for AI analysis
            violation_summary = self._create_violation_summary(violations)

            prompt = self._create_ai_prompt(violation_summary)

            plan_run = self.portia.run(prompt)
            result = plan_run.model_dump_json(indent=2)

            # Parse AI response and extract recommendations
            recommendations = self._parse_ai_response(result)

            if not recommendations:
                return self._generate_fallback_recommendations(violations)

            return recommendations
        except Exception as e:
            print(f"Error generating AI recommendations: {e}")
            return self._generate_fallback_recommendations(violations)

    def _create_violation_summary(self, violations: List[ComplianceViolation]) -> str:
        """Create a summary of violations for AI analysis"""
        if not violations:
            return "No violations found."

        # Group violations by severity
        # Group violations by severity
        critical_violations = [v for v in violations if v.severity == "critical"]
        high_violations     = [v for v in violations if v.severity == "high"]
        medium_violations   = [v for v in violations if v.severity == "medium"]
        low_violations      = [v for v in violations if v.severity == "low"]

        summary  = f"Found {len(violations)} compliance violations:\n"
        summary += f"- Critical severity: {len(critical_violations)}\n"
        summary += f"- High severity: {len(high_violations)}\n"
        summary += f"- Medium severity: {len(medium_violations)}\n"
        summary += f"- Low severity: {len(low_violations)}\n\n"

        # Add top violations by rule
        rule_violations = {}
        for violation in violations:
            if violation.rule_id not in rule_violations:
                rule_violations[violation.rule_id] = []
            rule_violations[violation.rule_id].append(violation)

        summary += "Top violations by rule:\n"
        for rule_id, rule_violations_list in list(rule_violations.items())[:5]:
            rule_title = rule_violations_list[0].rule_title
            count = len(rule_violations_list)
            summary += f"- {rule_title}: {count} violations\n"

        return summary

    def _create_ai_prompt(self, violation_summary: str) -> str:
        """Create AI prompt for analysis"""
        return f"""
        Based on these compliance violations found in a repository:
        
        {violation_summary}
        
        Please provide 5-7 actionable recommendations to improve the repository's security and compliance posture.
        Focus on:
        1. Immediate actions that can be taken
        2. Process improvements for the development team
        3. Tools and automation that should be implemented
        4. Training and awareness initiatives
        5. Long-term strategic improvements
        
        Format your response as a numbered list of specific, actionable recommendations.
        """

    def _parse_ai_response(self, ai_response: str) -> List[str]:
        """Parse AI response and extract recommendations"""
        try:
            # This is a simplified parser - you might want to implement more sophisticated parsing
            lines = ai_response.split("\n")
            recommendations = []

            for line in lines:
                line = line.strip()
                if line and (
                    line[0].isdigit() or line.startswith("-") or line.startswith("*")
                ):
                    # Remove numbering and clean up
                    clean_line = line.lstrip("0123456789.-* ").strip()
                    if clean_line and len(clean_line) > 10:
                        recommendations.append(clean_line)

            return recommendations[:7]  # Limit to 7 recommendations

        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return []

    def _generate_fallback_recommendations(
        self, violations: List[ComplianceViolation]
    ) -> List[str]:
        """Generate fallback recommendations when AI is not available"""
        recommendations = [
            "Implement automated security scanning in CI/CD pipeline",
            "Establish a secrets management policy and remove hardcoded credentials",
            "Regular dependency vulnerability assessments using tools like npm audit or pip-audit",
            "Security training for development team on secure coding practices",
            "Implement code review checklist specifically for security issues",
            "Set up automated compliance monitoring and reporting",
            "Create and maintain security documentation (SECURITY.md, security guidelines)",
        ]

        # Customize based on violations found
        if any(v.severity == "high" for v in violations):
            recommendations.insert(
                0, "URGENT: Address high-severity violations immediately"
            )

        if any("secrets" in v.rule_title.lower() for v in violations):
            recommendations.insert(1, "Implement secrets scanning in pre-commit hooks")

        return recommendations[:7]

    def analyze_violation_patterns(self, violations: List[ComplianceViolation]) -> dict:
        """Analyze patterns in violations for insights"""
        if not violations:
            return {}

        analysis = {
            "total_violations": len(violations),
            "severity_distribution": {},
            "rule_distribution": {},
            "file_type_distribution": {},
            "common_patterns": [],
        }

        # Analyze severity distribution
        for violation in violations:
            analysis["severity_distribution"][violation.severity] = (
                analysis["severity_distribution"].get(violation.severity, 0) + 1
            )

        # Analyze rule distribution
        for violation in violations:
            analysis["rule_distribution"][violation.rule_id] = (
                analysis["rule_distribution"].get(violation.rule_id, 0) + 1
            )

        # Analyze file type distribution
        for violation in violations:
            file_ext = (
                violation.file_path.split(".")[-1]
                if "." in violation.file_path
                else "no_extension"
            )
            analysis["file_type_distribution"][file_ext] = (
                analysis["file_type_distribution"].get(file_ext, 0) + 1
            )

        # Find common patterns
        high_frequency_rules = [
            rule_id
            for rule_id, count in analysis["rule_distribution"].items()
            if count > 2
        ]
        analysis["common_patterns"] = high_frequency_rules

        return analysis
