from pathlib import Path


class CodeIndexer:
    """
    Service responsible for discovering and reading source-code files
    from a cloned repository.
    """

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

    MAX_FILE_SIZE = 1_000_000  # 1 MB

    def index_repository(self, repository_path: str) -> list[dict]:
        """
        Discover and read supported source-code files.

        Returns a list of documents containing file metadata
        and source-code content.
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

        documents = []

        for path in root_path.rglob("*"):
            if not path.is_file():
                continue

            # Ignore generated, dependency, and Git directories
            if any(
                directory in self.IGNORED_DIRECTORIES
                for directory in path.parts
            ):
                continue

            language = self.LANGUAGE_MAP.get(path.suffix.lower())

            # Skip unsupported file types
            if not language:
                continue

            # Skip very large files
            try:
                if path.stat().st_size > self.MAX_FILE_SIZE:
                    continue
            except OSError:
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except (OSError, UnicodeDecodeError):
                continue

            relative_path = path.relative_to(root_path)

            documents.append(
                {
                    "file_path": str(relative_path),
                    "language": language,
                    "content": content,
                    "size": len(content),
                }
            )

        return documents