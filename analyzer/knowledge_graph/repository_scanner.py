from pathlib import Path

from analyzer.ast.parser_factory import (
    parse_source_file
)


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java"
}


def scan_repository(
    repository_path: str
) -> dict:
    """
    Scan the complete repository and extract
    AST information from every supported source file.
    """

    root = Path(repository_path)

    results = {}

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        relative_path = file_path.relative_to(
            root
        ).as_posix()

        source_code = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        ast_result = parse_source_file(
            relative_path,
            source_code
        )

        results[relative_path] = ast_result

    return results