from pathlib import Path

try:
    from git import Repo  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - handled at runtime
    Repo = None


class GitService:
    """
    Service responsible for cloning and managing Git repositories.
    """

    def __init__(self):
        self.base_path = Path("repositories")
        self.base_path.mkdir(exist_ok=True)

    def clone_repository(self, repo_url: str) -> str:
        """
        Clone a GitHub repository if it doesn't already exist.
        Returns the local path.
        """
        repo_name = repo_url.rstrip("/").split("/")[-1]
        target_path = self.base_path / repo_name

        if target_path.exists():
            return str(target_path)

        Repo.clone_from(repo_url, target_path)

        return str(target_path)