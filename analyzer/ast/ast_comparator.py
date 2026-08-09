from pathlib import Path

from .parser_factory import parse_source_file


def extract_source_lines(
    source_code: str,
    start_line: int,
    end_line: int
) -> str:
    """
    Extract the source-code section represented by an AST node.

    AST line numbers are converted to Python list indexes.
    """

    lines = source_code.splitlines()

    selected_lines = lines[
        start_line - 1:end_line
    ]

    return "\n".join(selected_lines).strip()


def build_entity_map(
    entities: list[dict]
) -> dict:
    """
    Convert a list of AST entities into a dictionary
    using the entity name as the key.
    """

    entity_map = {}

    for entity in entities:

        name = entity.get(
            "name",
            "anonymous"
        )

        # Keep the first occurrence of a name.
        if name not in entity_map:
            entity_map[name] = entity

    return entity_map


def compare_entities(
    original_entities: list[dict],
    modified_entities: list[dict],
    original_source: str,
    modified_source: str
) -> dict:
    """
    Compare AST entities such as functions or classes.

    Detects:
    - Added entities
    - Deleted entities
    - Modified entities
    - Unchanged entities
    """

    original_map = build_entity_map(
        original_entities
    )

    modified_map = build_entity_map(
        modified_entities
    )

    original_names = set(
        original_map.keys()
    )

    modified_names = set(
        modified_map.keys()
    )

    added_names = (
        modified_names - original_names
    )

    deleted_names = (
        original_names - modified_names
    )

    common_names = (
        original_names & modified_names
    )

    added = []
    deleted = []
    modified = []
    unchanged = []

    # Added entities
    for name in sorted(added_names):

        entity = modified_map[name]

        added.append({
            "name": name,
            "startLine": entity["startLine"],
            "endLine": entity["endLine"]
        })

    # Deleted entities
    for name in sorted(deleted_names):

        entity = original_map[name]

        deleted.append({
            "name": name,
            "startLine": entity["startLine"],
            "endLine": entity["endLine"]
        })

    # Compare entities existing in both versions.
    for name in sorted(common_names):

        original_entity = original_map[name]
        modified_entity = modified_map[name]

        original_code = extract_source_lines(
            original_source,
            original_entity["startLine"],
            original_entity["endLine"]
        )

        modified_code = extract_source_lines(
            modified_source,
            modified_entity["startLine"],
            modified_entity["endLine"]
        )

        if original_code != modified_code:

            modified.append({
                "name": name,
                "originalStartLine": (
                    original_entity["startLine"]
                ),
                "originalEndLine": (
                    original_entity["endLine"]
                ),
                "modifiedStartLine": (
                    modified_entity["startLine"]
                ),
                "modifiedEndLine": (
                    modified_entity["endLine"]
                )
            })

        else:

            unchanged.append(name)

    return {
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "unchanged": unchanged
    }


def compare_imports(
    original_imports: list[dict],
    modified_imports: list[dict]
) -> dict:
    """
    Compare imports between two source-code versions.
    """

    original_imports_set = {
        item["text"]
        for item in original_imports
    }

    modified_imports_set = {
        item["text"]
        for item in modified_imports
    }

    return {
        "added": sorted(
            modified_imports_set -
            original_imports_set
        ),
        "deleted": sorted(
            original_imports_set -
            modified_imports_set
        ),
        "unchanged": sorted(
            original_imports_set &
            modified_imports_set
        )
    }


def compare_ast_sources(
    file_path: str,
    original_source: str,
    modified_source: str
) -> dict:
    """
    Parse and structurally compare two versions
    of the same source-code file.
    """

    original_ast = parse_source_file(
        file_path,
        original_source
    )

    modified_ast = parse_source_file(
        file_path,
        modified_source
    )

    if not original_ast["supported"]:
        return {
            "supported": False,
            "message": (
                "Unsupported programming language."
            )
        }

    function_comparison = compare_entities(
        original_ast["functions"],
        modified_ast["functions"],
        original_source,
        modified_source
    )

    class_comparison = compare_entities(
        original_ast["classes"],
        modified_ast["classes"],
        original_source,
        modified_source
    )

    import_comparison = compare_imports(
        original_ast["imports"],
        modified_ast["imports"]
    )

    return {
        "supported": True,
        "language": original_ast["language"],

        "functions": function_comparison,

        "classes": class_comparison,

        "imports": import_comparison,

        "syntaxErrors": {
            "original": original_ast["errors"],
            "modified": modified_ast["errors"]
        }
    }