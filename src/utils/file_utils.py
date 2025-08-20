import os
import hashlib
from pathlib import Path
from typing import List, Optional


class FileUtils:
    """Utility functions for file operations"""

    @staticmethod
    def get_file_hash(file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            return file_hash.hexdigest()
        except Exception:
            return ""

    @staticmethod
    def is_text_file(file_path: Path) -> bool:
        """Check if file is likely a text file"""
        try:
            # Check file extension
            text_extensions = {
                ".txt",
                ".md",
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
                ".sh",
                ".bat",
                ".ps1",
                ".sql",
                ".r",
                ".m",
                ".go",
                ".rs",
                ".php",
                ".rb",
                ".pl",
            }

            if file_path.suffix.lower() in text_extensions:
                return True

            # Check file content (first 1024 bytes)
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                try:
                    chunk.decode("utf-8")
                    return True
                except UnicodeDecodeError:
                    return False

        except Exception:
            return False

    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Get file size in megabytes"""
        try:
            return file_path.stat().st_size / (1024 * 1024)
        except Exception:
            return 0.0

    @staticmethod
    def should_skip_file(file_path: Path, max_size_mb: float = 10.0) -> bool:
        """Determine if a file should be skipped during scanning"""
        # Skip files that are too large
        if FileUtils.get_file_size_mb(file_path) > max_size_mb:
            return True

        # Skip binary files
        if not FileUtils.is_text_file(file_path):
            return True

        return False

    @staticmethod
    def find_files_by_pattern(directory: Path, pattern: str) -> List[Path]:
        """Find files matching a pattern in directory"""
        try:
            return list(directory.glob(pattern))
        except Exception:
            return []

    @staticmethod
    def get_relative_path(file_path: Path, base_path: Path) -> str:
        """Get relative path from base path"""
        try:
            return str(file_path.relative_to(base_path))
        except ValueError:
            return str(file_path)
