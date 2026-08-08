from pathlib import Path
from difflib import SequenceMatcher


# File extensions that represent source-code/text files
SOURCE_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".css",
    ".scss",
    ".html",
    ".json",
}


def is_source_file(file_path: Path) -> bool:
    """
    Check whether the file is a supported source-code file.
    """

    return file_path.suffix.lower() in SOURCE_EXTENSIONS


def read_file_lines(file_path: Path) -> list[str]:
    """
    Read a text file and return its contents as individual lines.
    """

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()


def compare_lines(
    original_file: str,
    modified_file: str
) -> dict:
    """
    Compare two source files line by line.

    Returns:
        Number of added lines
        Number of deleted lines
        Number of changed lines
        Detailed change information
    """

    original_path = Path(original_file)
    modified_path = Path(modified_file)

    # Ignore files that are not source-code files.
    if not is_source_file(original_path):
        return {
            "isSourceFile": False,
            "linesAdded": 0,
            "linesDeleted": 0,
            "linesChanged": 0,
            "changes": []
        }

    original_lines = read_file_lines(original_path)
    modified_lines = read_file_lines(modified_path)

    # Compare the sequence of lines in both files.
    matcher = SequenceMatcher(
        None,
        original_lines,
        modified_lines
    )

    lines_added = 0
    lines_deleted = 0
    lines_changed = 0

    changes = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        # No change in this section.
        if tag == "equal":
            continue

        # New lines were added.
        if tag == "insert":

            added_count = j2 - j1

            lines_added += added_count

            changes.append({
                "type": "added",
                "originalStartLine": None,
                "originalEndLine": None,
                "modifiedStartLine": j1 + 1,
                "modifiedEndLine": j2,
                "addedLines": modified_lines[j1:j2],
                "deletedLines": []
            })

        # Existing lines were deleted.
        elif tag == "delete":

            deleted_count = i2 - i1

            lines_deleted += deleted_count

            changes.append({
                "type": "deleted",
                "originalStartLine": i1 + 1,
                "originalEndLine": i2,
                "modifiedStartLine": None,
                "modifiedEndLine": None,
                "addedLines": [],
                "deletedLines": original_lines[i1:i2]
            })

        # Existing lines were replaced/modified.
        elif tag == "replace":

            deleted_count = i2 - i1
            added_count = j2 - j1

            lines_deleted += deleted_count
            lines_added += added_count

            # Count the overlapping lines as changed.
            lines_changed += min(
                deleted_count,
                added_count
            )

            changes.append({
                "type": "modified",
                "originalStartLine": i1 + 1,
                "originalEndLine": i2,
                "modifiedStartLine": j1 + 1,
                "modifiedEndLine": j2,
                "addedLines": modified_lines[j1:j2],
                "deletedLines": original_lines[i1:i2]
            })

    return {
        "isSourceFile": True,
        "linesAdded": lines_added,
        "linesDeleted": lines_deleted,
        "linesChanged": lines_changed,
        "changes": changes
    }