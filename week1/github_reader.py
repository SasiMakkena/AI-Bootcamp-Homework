import io
import zipfile
import traceback
from dataclasses import dataclass
from typing import Iterable, Callable, Optional, List

import requests


@dataclass
class RawRepositoryFile:
    filename: str
    content: str


class GithubRepositoryDataReader:
    """
    Downloads and filters files from a GitHub repository (via codeload ZIP).
    """

    def __init__(
        self,
        repo_owner: str,
        repo_name: str,
        allowed_extensions: Optional[Iterable[str]] = None,
        filename_filter: Optional[Callable[[str], bool]] = None,
    ):
        """
        Args:
            repo_owner: GitHub org/user
            repo_name: repository name
            allowed_extensions: e.g. {"md", "py"} (None = any)
            filename_filter: function(filepath) -> bool (None = keep all)
        """
        prefix = "https://codeload.github.com"
        self.url = f"{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main"

        # Ensure attributes always exist
        if allowed_extensions is not None:
            self.allowed_extensions = {ext.lower() for ext in allowed_extensions}
        else:
            self.allowed_extensions = None

        if filename_filter is None:
            self.filename_filter = lambda filepath: True
        else:
            self.filename_filter = filename_filter

    def read(self) -> List[RawRepositoryFile]:
        """Download and extract repository files."""
        resp = requests.get(self.url)
        if resp.status_code != 200:
            raise Exception(f"Failed to download repository: {resp.status_code}")

        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        try:
            repository_data = self._extract_files(zf)
        finally:
            zf.close()
        return repository_data

    def _extract_files(self, zf: zipfile.ZipFile) -> List[RawRepositoryFile]:
        """Extract and process files from the zip archive."""
        data: List[RawRepositoryFile] = []

        for file_info in zf.infolist():
            filepath = self._normalize_filepath(file_info.filename)

            if self._should_skip_file(filepath):
                continue

            try:
                with zf.open(file_info) as f_in:
                    content = f_in.read().decode("utf-8", errors="ignore")
                    content = content.strip() if content is not None else ""
                    data.append(RawRepositoryFile(filename=filepath, content=content))
            except Exception as e:
                print(f"Error processing {file_info.filename}: {e}")
                traceback.print_exc()
                continue

        return data

    def _should_skip_file(self, filepath: str) -> bool:
        filepath_lower = filepath.lower()

        # directory
        if filepath_lower.endswith("/"):
            return True

        # hidden file at end
        filename = filepath_lower.split("/")[-1]
        if filename.startswith("."):
            return True

        # extension filter
        if self.allowed_extensions:
            ext = self._get_extension(filepath_lower)
            if ext not in self.allowed_extensions:
                return True

        # caller filter
        if not self.filename_filter(filepath):
            return True

        return False

    @staticmethod
    def _get_extension(filepath: str) -> str:
        filename = filepath.split("/")[-1]
        if "." in filename:
            return filename.rsplit(".", maxsplit=1)[-1]
        return ""

    @staticmethod
    def _normalize_filepath(filepath: str) -> str:
        # 'repo-main/path/to/file.py' -> 'path/to/file.py'
        parts = filepath.split("/", maxsplit=1)
        return parts[1] if len(parts) > 1 else parts[0]
