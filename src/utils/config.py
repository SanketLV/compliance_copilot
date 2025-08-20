import os
from pathlib import Path
from typing import Dict, Any


def load_env():
    """Load environment variables from .env file"""
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        print(
            "Warning: python-dotenv not installed. Environment variables may not be loaded."
        )


def get_config() -> Dict[str, Any]:
    """Get configuration settings"""
    config = {
        "rules_file": "config/rules.json",
        "output_dir": "reports",
        "excluded_dirs": [".git", "node_modules", "venv", "__pycache__"],
        "excluded_files": [".DS_Store", "Thumbs.db"],
        "max_file_size_mb": 10,  # Skip files larger than this
        "supported_extensions": [
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".yml",
            ".yaml",
            ".json",
            ".xml",
            ".html",
            ".css",
        ],
        "ai_enabled": bool(os.getenv("GOOGLE_API_KEY")),
        "scan_timeout_seconds": 300,  # 5 minutes
    }

    return config


def get_rules_file_path() -> Path:
    """Get the path to the rules file"""
    config = get_config()
    rules_path = Path(config["rules_file"])

    # Try relative to current working directory
    if rules_path.exists():
        return rules_path

    # Try relative to script location
    script_dir = Path(__file__).parent.parent.parent
    rules_path = script_dir / config["rules_file"]

    if rules_path.exists():
        return rules_path

    # Fallback to current directory
    return Path("rules.json")
