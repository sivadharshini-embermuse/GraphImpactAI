import json
from pathlib import Path


def create_change_summary(
    comparison_result: dict,
    output_path: str
) -> dict:
    """
    Create and save the repository comparison summary.
    """

    summary = {
        "summary": {
            "addedFilesCount": len(
                comparison_result["addedFiles"]
            ),
            "deletedFilesCount": len(
                comparison_result["deletedFiles"]
            ),
            "modifiedFilesCount": len(
                comparison_result["modifiedFiles"]
            ),
            "unchangedFilesCount": len(
                comparison_result["unchangedFiles"]
            )
        },
        "changes": comparison_result
    }

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
            summary,
            file,
            indent=4
        )

    return summary

    file_changes = comparison_result.get(
        "fileChanges",
        {}
    )

    total_lines_added = sum(
        change["linesAdded"]
        for change in file_changes.values()
    )

    total_lines_deleted = sum(
        change["linesDeleted"]
        for change in file_changes.values()
    )

    total_lines_changed = sum(
        change["linesChanged"]
        for change in file_changes.values()
    )

    summary = {
        "summary": {
            "addedFilesCount": len(
                comparison_result["addedFiles"]
            ),
            "deletedFilesCount": len(
                comparison_result["deletedFiles"]
            ),
            "modifiedFilesCount": len(
                comparison_result["modifiedFiles"]
            ),
            "unchangedFilesCount": len(
                comparison_result["unchangedFiles"]
            ),
            "linesAdded": total_lines_added,
            "linesDeleted": total_lines_deleted,
            "linesChanged": total_lines_changed
        },
        "changes": comparison_result
    }





"""
Change Summary Module
Generates a unified JSON Change Summary Report combining file, function, import, and AST diffs.
"""
