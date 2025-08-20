from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class RepositoryInfo:
    """Information about a repository being analyzed"""

    url: str
    name: str
    local_path: Path
    branch: str
    commit_hash: Optional[str] = None
    size_bytes: Optional[int] = None
    file_count: Optional[int] = None

    def get_relative_path(self, file_path: Path) -> str:
        """Get relative path from repository root"""
        try:
            return str(file_path.relative_to(self.local_path))
        except ValueError:
            return str(file_path)
