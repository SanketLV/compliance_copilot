# Repository Compliance Copilot 🚀

A comprehensive, AI-powered tool for checking repository compliance against security, governance, and best practice rules. Built with a modular architecture for easy maintenance and extensibility.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Compliance Rules](#-compliance-rules)
- [API Reference](#-api-reference)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

- 🔍 **Automated Repository Scanning**: Downloads and analyzes repositories from GitHub/GitLab
- 🧠 **AI-Powered Analysis**: Uses Google Gemini for intelligent recommendations
- 📊 **Comprehensive Reporting**: Multiple output formats (JSON, Markdown, Console)
- 🎯 **Configurable Rules**: Easy-to-modify compliance rules with pattern matching
- 🏗️ **Modular Architecture**: Clean separation of concerns for maintainability
- 🔒 **Security Focus**: Built-in rules covering SOC2, OWASP, CIS, and more
- 📈 **Compliance Scoring**: Quantitative assessment with severity-based weighting
- ⚡ **High Performance**: Efficient file scanning with configurable exclusions

## 🏗️ Project Structure

```
repo-compliance-copilot/
├── src/                          # Source code
│   ├── models/                   # Data models and structures
│   │   ├── compliance.py        # Compliance rule and violation models
│   │   ├── repository.py        # Repository information models
│   │   └── __init__.py          # Model exports
│   ├── core/                     # Core business logic
│   │   ├── rule_engine.py       # Rule management and pattern matching
│   │   ├── scanner.py           # File scanning and violation detection
│   │   ├── downloader.py        # Repository download and extraction
│   │   └── __init__.py          # Core module exports
│   ├── services/                 # High-level services
│   │   ├── ai_analyzer.py       # AI-powered analysis and recommendations
│   │   ├── report_generator.py  # Report generation in multiple formats
│   │   └── __init__.py          # Service exports
│   ├── utils/                    # Utility functions
│   │   ├── config.py            # Configuration management
│   │   ├── file_utils.py        # File operation utilities
│   │   └── __init__.py          # Utility exports
│   ├── compliance_checker.py    # Main orchestrator class
│   └── __init__.py              # Package initialization
├── config/                       # Configuration files
│   └── rules.json               # Compliance rules definition
├── tests/                        # Test suite
│   ├── test_rule_engine.py      # Rule engine tests
│   └── __init__.py              # Test package
├── reports/                      # Generated reports (auto-created)
├── main.py                       # Command-line entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **Git** for version control
- **Google API Key** for Gemini AI features (optional but recommended)

### Step-by-Step Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SanketLV/compliance_copilot
   cd compliance-copilot
   ```

2. **Create virtual environment** (recommended):

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

   **Note**: Replace `your_google_api_key_here` with your actual Google API key for Gemini access.

## 🚀 Quick Start

### Basic Usage

```bash
# Interactive mode - prompts for repository URL
python main.py

# Check specific repository
python main.py -u https://github.com/username/repo

# Generate quick summary only
python main.py --summary -u https://github.com/username/repo
```

### First Run Example

```bash
$ python main.py -u https://github.com/username/sample-repo

Starting compliance check for: https://github.com/username/sample-repo
Downloading GitHub repository: https://github.com/username/sample-repo/archive/main.zip
Repository extracted to: /tmp/tmpXXXXXX/extracted/sample-repo-main
Loaded 10 compliance rules from config/rules.json
Scanning repository: sample-repo
Scanned 45 files, found 3 violations

================================================================================
REPOSITORY COMPLIANCE REPORT
================================================================================
Repository: sample-repo
Compliance Score: 92.5/100
Total Violations: 3
High Severity: 1
Medium Severity: 1
Low Severity: 1

Reports saved:
  JSON: reports/compliance_report_sample-repo_20241201_143022.json
  Markdown: reports/compliance_report_sample-repo_20241201_143022.md
```

## 🎯 Usage

### Command Line Options

| Option             | Description                   | Example                                     |
| ------------------ | ----------------------------- | ------------------------------------------- |
| `-u, --url`        | Repository URL to check       | `-u https://github.com/user/repo`           |
| `--summary`        | Generate quick summary only   | `--summary -u https://github.com/user/repo` |
| `--validate-rules` | Validate all compliance rules | `--validate-rules`                          |
| `--rules-file`     | Custom rules file path        | `--rules-file custom_rules.json`            |
| `--output-dir`     | Output directory for reports  | `--output-dir ./my_reports`                 |
| `--help`           | Show help message             | `--help`                                    |

### Usage Modes

#### 1. **Full Compliance Check** (Default)

```bash
python main.py -u https://github.com/username/repo
```

- Downloads repository
- Scans all files against compliance rules
- Generates AI recommendations
- Creates detailed reports (JSON + Markdown)
- Displays console summary

#### 2. **Quick Summary Mode**

```bash
python main.py --summary -u https://github.com/username/repo
```

- Faster execution
- Basic violation count and severity breakdown
- No detailed reports generated
- Ideal for CI/CD integration

#### 3. **Rules Validation Mode**

```bash
python main.py --validate-rules
```

- Validates all compliance rules
- Checks syntax and configuration
- Reports any errors or issues
- Useful for rule maintenance

#### 4. **Interactive Mode**

```bash
python main.py
```

- Prompts for repository URL
- Full compliance check
- User-friendly interface

### Advanced Usage

#### Custom Rules File

```bash
python main.py -u https://github.com/user/repo --rules-file ./custom_rules.json
```

#### Custom Output Directory

```bash
python main.py -u https://github.com/user/repo --output-dir ./compliance_reports
```

#### Batch Processing (Script)

```bash
#!/bin/bash
repos=(
    "https://github.com/user/repo1"
    "https://github.com/user/repo2"
    "https://gitlab.com/user/repo3"
)

for repo in "${repos[@]}"; do
    echo "Checking: $repo"
    python main.py -u "$repo" --output-dir ./batch_reports
done
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required for AI features
GOOGLE_API_KEY=your_google_api_key_here

# Optional customizations
COMPLIANCE_OUTPUT_DIR=./my_reports
COMPLIANCE_RULES_FILE=./custom_rules.json
COMPLIANCE_SCAN_TIMEOUT=600
```

### Configuration File

The system automatically detects configuration from `src/utils/config.py`:

```python
# Default configuration
config = {
    'rules_file': 'config/rules.json',
    'output_dir': 'reports',
    'excluded_dirs': ['.git', 'node_modules', 'venv', '__pycache__'],
    'excluded_files': ['.DS_Store', 'Thumbs.db'],
    'max_file_size_mb': 10,
    'supported_extensions': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.yml', '.yaml', '.json', '.xml', '.html', '.css'],
    'ai_enabled': bool(os.getenv("GOOGLE_API_KEY")),
    'scan_timeout_seconds': 300,
}
```

## 🔒 Compliance Rules

### Built-in Rules

The system includes 10 comprehensive compliance rules:

| Rule ID  | Title                  | Severity | Description                                  |
| -------- | ---------------------- | -------- | -------------------------------------------- |
| **R001** | Secrets Detection      | High     | Detect API keys, private keys, .env files    |
| **R002** | Dependency Risks       | High     | Check for outdated/vulnerable dependencies   |
| **R003** | Dockerfile Security    | High     | Detect insecure Docker images and root usage |
| **R004** | CI/CD Security Steps   | Medium   | Detect missing security scans in pipelines   |
| **R005** | Public Config Files    | High     | Detect sensitive configuration files         |
| **R006** | Logging PII            | High     | Detect sensitive data in logs                |
| **R007** | Weak Authentication    | High     | Detect hardcoded weak credentials            |
| **R008** | Insecure HTTP Usage    | Medium   | Detect plain HTTP URLs                       |
| **R009** | Missing Security Files | Low      | Check for SECURITY.md, .gitignore            |
| **R010** | License & Compliance   | Low      | Check for LICENSE and README files           |

### Rule Structure

Each rule follows this JSON structure:

```json
{
  "id": "R001",
  "title": "Secrets Detection",
  "description": "Detect committed secrets like API keys, private keys, or .env files.",
  "file_patterns": [".env", ".pem", ".p12", "id_rsa", "id_dsa"],
  "regex_patterns": [
    "(?i)(aws|gcp|stripe|github).*?(key|secret).*?['\"][0-9a-zA-Z\\-_]{16,}['\"]"
  ],
  "severity": "high",
  "compliance_mapping": ["SOC2 CC6.1", "OWASP A02"],
  "fix_suggestion": "Remove secrets from repo, rotate keys, and use a secret manager."
}
```

### Adding Custom Rules

1. **Edit `config/rules.json`**:

   ```json
   {
     "id": "R011",
     "title": "Custom Rule",
     "description": "Your custom compliance rule",
     "file_patterns": ["*.py", "*.js"],
     "regex_patterns": ["your_pattern"],
     "severity": "medium",
     "compliance_mapping": ["SOC2 CC6.1"],
     "fix_suggestion": "How to fix this issue"
   }
   ```

2. **Restart the application** or use `--rules-file` option

### Rule Validation

```bash
# Validate all rules
python main.py --validate-rules

# Example output
Validating compliance rules...
Loaded 10 compliance rules from config/rules.json

Validation Results:
Total Rules: 10
Valid Rules: 10
Invalid Rules: 0
```

## 🔧 API Reference

### Core Classes

#### `ComplianceChecker`

Main orchestrator class for repository compliance checking.

```python
from src.compliance_checker import ComplianceChecker

# Initialize
checker = ComplianceChecker()

# Check repository
report = checker.check_repository("https://github.com/user/repo")

# Get summary
summary = checker.get_compliance_summary("https://github.com/user/repo")

# Validate rules
validation = checker.validate_rules()
```

#### `RuleEngine`

Manages compliance rules and pattern matching.

```python
from src.core.rule_engine import RuleEngine

engine = RuleEngine("config/rules.json")
rules = engine.get_rules()
rule = engine.get_rule_by_id("R001")
```

#### `ComplianceScanner`

Scans repository files for compliance violations.

```python
from src.core.scanner import ComplianceScanner

scanner = ComplianceScanner(rule_engine)
violations = scanner.scan_repository(repo_info)
```

### Data Models

#### `ComplianceRule`

```python
@dataclass
class ComplianceRule:
    id: str
    title: str
    description: str
    file_patterns: List[str]
    regex_patterns: List[str]
    severity: str
    compliance_mapping: List[str]
    fix_suggestion: str
```

#### `ComplianceViolation`

```python
@dataclass
class ComplianceViolation:
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
```

#### `ComplianceReport`

```python
@dataclass
class ComplianceReport:
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
```

## 🧪 Development

### Setting Up Development Environment

1. **Clone and setup**:

   ```bash
   git clone https://github.com/SanketLV/compliance_copilot
   cd compliance_copilot
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Install development dependencies**:

   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

3. **Set up pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_rule_engine.py -v

# Run with verbose output
pytest tests/ -v -s
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Project Structure Guidelines

- **Models** (`src/models/`): Data structures and validation
- **Core** (`src/core/`): Business logic and algorithms
- **Services** (`src/services/`): High-level operations and external integrations
- **Utils** (`src/utils/`): Helper functions and configuration
- **Tests** (`tests/`): Comprehensive test coverage

### Adding New Features

1. **Create feature branch**:

   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement feature** following existing patterns
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Submit pull request**

## 🐛 Troubleshooting

### Common Issues

#### 1. **Import Errors**

```bash
Error: No module named 'src'
```

**Solution**: Ensure you're running from the project root directory.

#### 2. **Google API Key Issues**

```bash
Warning: GOOGLE_API_KEY not found. AI analysis will be limited.
```

**Solution**:

- Check `.env` file exists
- Verify API key is correct
- Ensure Google Gemini API is enabled

#### 3. **Repository Download Failures**

```bash
Error: Failed to download repository
```

**Solutions**:

- Check repository URL format
- Verify repository is public
- Check internet connection
- Try different repository

#### 4. **Rule Loading Errors**

```bash
Error: No compliance rules loaded
```

**Solutions**:

- Verify `config/rules.json` exists
- Check JSON syntax
- Use `--validate-rules` to debug

#### 5. **Permission Errors**

```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions**:

- Check file permissions
- Run with appropriate user privileges
- Verify output directory is writable

### Debug Mode

Enable verbose logging:

```bash
# Set environment variable
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run with debug output
python -u main.py -u https://github.com/user/repo 2>&1 | tee debug.log
```

### Performance Issues

- **Large repositories**: Use `--summary` mode for quick checks
- **Slow scanning**: Check excluded directories configuration
- **Memory issues**: Reduce `max_file_size_mb` in config

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the coding standards
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Standards

- **Code Style**: Follow PEP 8 and use Black for formatting
- **Type Hints**: Use type hints for all function parameters and returns
- **Documentation**: Include docstrings for all public functions
- **Testing**: Maintain >90% test coverage
- **Commits**: Use conventional commit messages

### Areas for Contribution

- **New Compliance Rules**: Add industry-specific compliance frameworks
- **Repository Sources**: Support for additional Git platforms
- **AI Integration**: Enhance AI analysis capabilities
- **Performance**: Optimize scanning and analysis algorithms
- **Documentation**: Improve user guides and API documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini** for AI-powered analysis
- **OWASP** for security best practices
- **SOC2** framework for compliance standards
- **CIS** for Docker security guidelines

## 📞 Support

### Getting Help

1. **Check the documentation** first
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

### Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/SanketLV/compliance_copilot/issues)
- **Discussions**: [Join community discussions](https://github.com/SanketLV/compliance_copilot/discussions)

---

**Made with ❤️ by Sanket Lakhani**

_Empowering developers to build secure, compliant, and trustworthy software._
