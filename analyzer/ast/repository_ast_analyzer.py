import json
from pathlib import Path

from analyzer.comparison.compare_files import (
    compare_files,
    resolve_repository_root
)

from analyzer.ast.parser_factory import (
    parse_source_file
)

from analyzer.ast.ast_comparator import (
    compare_ast_sources
)


def read_source_file(file_path: Path) -> str:
    """
    Read a source-code file as UTF-8 text.
    """

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def analyze_changed_files(
    original_repository: str,
    modified_repository: str
) -> dict:
    """
    Analyze AST-level changes for all modified
    source-code files in two repositories.
    """

    # Compare repositories first.
    comparison = compare_files(
        original_repository,
        modified_repository
    )

    # IMPORTANT:
    # Use the same repository-root resolution logic
    # used by compare_files().
    original_root = resolve_repository_root(
        Path(original_repository)
    )

    modified_root = resolve_repository_root(
        Path(modified_repository)
    )

    ast_results = {}

    for relative_file in comparison["modifiedFiles"]:

        original_file = (
            original_root / relative_file
        )

        modified_file = (
            modified_root / relative_file
        )

        # Check that both files actually exist.
        if not original_file.exists():
            ast_results[relative_file] = {
                "supported": False,
                "error": (
                    "Original file not found: "
                    f"{original_file}"
                )
            }

            continue

        if not modified_file.exists():
            ast_results[relative_file] = {
                "supported": False,
                "error": (
                    "Modified file not found: "
                    f"{modified_file}"
                )
            }

            continue

        # Detect language using the file extension.
        language_info = parse_source_file(
            relative_file,
            ""
        )

        if not language_info["supported"]:
            ast_results[relative_file] = {
                "supported": False,
                "message": (
                    "Unsupported programming language."
                )
            }

            continue

        # Read both versions of the file.
        original_source = read_source_file(
            original_file
        )

        modified_source = read_source_file(
            modified_file
        )

        # Perform structural AST comparison.
        result = compare_ast_sources(
            relative_file,
            original_source,
            modified_source
        )

        ast_results[relative_file] = result

    return {
        "modifiedFilesCount": len(
            comparison["modifiedFiles"]
        ),
        "analyzedFilesCount": len(
            ast_results
        ),
        "results": ast_results
    }


def save_analysis_result(
    result: dict,
    output_path: str
) -> None:
    """
    Save AST analysis results as JSON.
    """

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )


def main():

    import sys

    if len(sys.argv) != 3:

        print(
            "Usage: python -m "
            "analyzer.ast.repository_ast_analyzer "
            "<original_repository> "
            "<modified_repository>"
        )

        return

    original_repository = sys.argv[1]
    modified_repository = sys.argv[2]

    result = analyze_changed_files(
        original_repository,
        modified_repository
    )

    output_path = (
        "analyzer/data/outputs/"
        "ast_analysis.json"
    )

    save_analysis_result(
        result,
        output_path
    )

    print(
        "\n========== AST REPOSITORY ANALYSIS ==========\n"
    )

    print(
        f"Modified files : "
        f"{result['modifiedFilesCount']}"
    )

    print(
        f"Analyzed files : "
        f"{result['analyzedFilesCount']}"
    )

    print(
        f"\nAST report saved to: {output_path}"
    )


if __name__ == "__main__":
    main()