from pathlib import Path


def normalize_import_path(
    current_file: str,
    import_text: str
) -> str | None:
    """
    Convert a relative import into a normalized
    repository-relative path.

    Example:

        src/App.js
        ../services/UserService

    becomes:

        services/UserService
    """

    current_path = Path(current_file)

    import_value = import_text.strip()

    # Ignore external packages.
    if not import_value.startswith("."):
        return None

    current_directory = current_path.parent

    resolved_path = (
        current_directory / import_value
    ).as_posix()

    normalized = Path(
        resolved_path
    ).as_posix()

    return normalized


def extract_import_dependencies(
    file_path: str,
    ast_result: dict
) -> list[dict]:
    """
    Extract import dependencies from AST information.

    Only relative/local imports are considered
    repository dependencies.
    """

    dependencies = []

    for import_item in ast_result.get(
        "imports",
        []
    ):

        import_text = import_item.get(
            "text",
            ""
        )

        dependency_path = normalize_import_path(
            file_path,
            import_text
        )

        if dependency_path is None:
            continue

        dependencies.append({
            "source": file_path,
            "target": dependency_path,
            "type": "imports",
            "line": import_item.get(
                "startLine"
            ),
            "statement": import_text
        })

    return dependencies