from pathlib import Path
from collections import Counter


class AnalyzerService:
    """
    Service responsible for analyzing a cloned repository.
    """

    # File extensions mapped to programming languages
    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".go": "Go",
        ".rs": "Rust",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".cs": "C#",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".kts": "Kotlin",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".sql": "SQL",
        ".sh": "Shell",
    }

    # Files that help identify the project structure
    IMPORTANT_FILES = {
        "README.md": "readme",
        "README": "readme",
        "Dockerfile": "dockerfile",
        "docker-compose.yml": "docker_compose",
        "docker-compose.yaml": "docker_compose",
        "package.json": "package_json",
        "requirements.txt": "requirements_txt",
        "pyproject.toml": "pyproject_toml",
        "package-lock.json": "package_lock",
        "yarn.lock": "yarn_lock",
        "pnpm-lock.yaml": "pnpm_lock",
        "go.mod": "go_mod",
        "Cargo.toml": "cargo_toml",
    }

    # Directories that should not be analyzed
    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "dist",
        "build",
        "target",
    }

    def analyze_repository(self, repository_path: str) -> dict:
        """
        Analyze a cloned repository and return structured metadata.

        Args:
            repository_path: Local path of the cloned repository.

        Returns:
            Dictionary containing repository statistics and metadata.
        """
        root_path = Path(repository_path)

        if not root_path.exists():
            raise FileNotFoundError(
                f"Repository path does not exist: {repository_path}"
            )

        if not root_path.is_dir():
            raise ValueError(
                f"Repository path is not a directory: {repository_path}"
            )

        total_files = 0
        language_counter = Counter()

        detected_files = {
            "readme": False,
            "dockerfile": False,
            "docker_compose": False,
            "package_json": False,
            "requirements_txt": False,
            "pyproject_toml": False,
            "package_lock": False,
            "yarn_lock": False,
            "pnpm_lock": False,
            "go_mod": False,
            "cargo_toml": False,
        }

        for path in root_path.rglob("*"):
            if not path.is_file():
                continue

            # Ignore files inside excluded directories
            if any(
                directory in self.IGNORED_DIRECTORIES
                for directory in path.parts
            ):
                continue

            total_files += 1

            # Detect programming language
            language = self.LANGUAGE_MAP.get(path.suffix.lower())

            if language:
                language_counter[language] += 1

            # Detect important project files
            file_name = path.name

            if file_name in self.IMPORTANT_FILES:
                metadata_key = self.IMPORTANT_FILES[file_name]
                detected_files[metadata_key] = True

        return {
            "repository_path": str(root_path),
            "total_files": total_files,
            "languages": dict(language_counter),
            "detected_files": detected_files,
        }