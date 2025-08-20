import os
import tempfile
import zipfile
import requests
from pathlib import Path
from typing import Optional
from ..models.repository import RepositoryInfo
from ..utils.config import get_config


class RepositoryDownloader:
    """Handles downloading and extracting repositories from various sources"""

    def __init__(self):
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Repository-Compliance-copilot/1.0"})

    def download_repository(self, repo_url: str) -> Optional[RepositoryInfo]:
        """Download repository from URL and return repository info"""
        try:
            if "github.com" in repo_url:
                return self._download_github_repo(repo_url)
            elif "gitlab.com" in repo_url:
                return self._download_gitlab_repo(repo_url)
            else:
                print(f"Unsupported repository URL: {repo_url}")
                return None
        except Exception as e:
            print(f"Error downloading repository: {e}")
            return None

    def _download_github_repo(self, repo_url: str) -> Optional[RepositoryInfo]:
        """Download repository from github"""
        try:
            # Clean up github URl
            if repo_url.endswith(".git"):
                repo_url = repo_url[:-4]

            # Extract repository name
            repo_name = repo_url.split("/")[-1]

            # Create download URL
            download_url = f"{repo_url}/archive/main.zip"

            print(f"Downloading Github repository: {download_url}")

            # Downlaod and extract
            repo_info = self._download_and_extract(download_url, repo_name)
            if repo_info:
                repo_info.branch = "main"

            return repo_info

        except Exception as e:
            print(f"Error downloading Github repository: {e}")
            return None

    def _download_gitlab_repo(self, repo_url: str) -> Optional[RepositoryInfo]:
        """Download repository from gitlab"""
        try:
            # Clean up gitlab URl
            if repo_url.endswith(".git"):
                repo_url = repo_url[:-4]

            # Extract repository name
            repo_name = repo_url.split("/")[-1]

            # Create download URL
            download_url = f"{repo_url}/-/archive/main/main.zip"

            print(f"Downloading Gitlab repository: {download_url}")

            # Downlaod and extract
            repo_info = self._download_and_extract(download_url, repo_name)
            if repo_info:
                repo_info.branch = "main"

            return repo_info

        except Exception as e:
            print(f"Error downloading Gitlab repository: {e}")
            return None

    def _download_and_extract(
        self, download_url: str, repo_name: str
    ) -> Optional[RepositoryInfo]:
        """Download and extract repository archieve"""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            zip_path = Path(temp_dir) / "repo.zip"

            # Download the repository
            response = self.session.get(download_url, stream=True)
            response.raise_for_status()

            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Extract the repository
            extract_dir = Path(temp_dir) / "extracted"
            extract_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            # Find the actual repository directory
            extracted_items = list(extract_dir.iterdir())
            if len(extracted_items) == 1 and extracted_items[0].is_dir():
                repo_dir = extracted_items[0]
            else:
                repo_dir = extract_dir

            # Calculate repository size
            size_bytes = self._calculate_directory_size(repo_dir)
            file_count = self._count_files(repo_dir)

            print(f"Repository extracted to: {repo_dir}")
            print(f"Size: {size_bytes / (1024*1024):.2f} MB, Files: {file_count}")

            return RepositoryInfo(
                url=download_url,
                name=repo_name,
                local_path=repo_dir,
                branch="main",
                size_bytes=size_bytes,
                file_count=file_count,
            )
        except Exception as e:
            print(f"Error in download and extract: {e}")
            return None

    def _calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory in bytes"""
        total_size = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass

        return total_size

    def _count_files(self, directory: Path) -> int:
        """Count total number of files in directory"""
        try:
            return len([f for f in directory.rglob("*") if f.is_file()])
        except Exception:
            return 0

    def cleanup(self, repo_info: RepositoryInfo) -> None:
        """Clean Up temporary repository files"""
        try:
            if repo_info.local_path.exists():
                # Remove the entire temp directory
                temp_dir = repo_info.local_path.parents[1]
                import shutil

                shutil.rmtree(temp_dir)
                print("Temporary files cleaned up")
        except Exception as e:
            print(f"Error cleaning up: {e}")
