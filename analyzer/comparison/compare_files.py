from pathlib import Path
import hashlib

from .compare_lines import compare_lines


def resolve_repository_root(repository_path: Path) -> Path:
    """
    Resolve unnecessary wrapper folders inside an extracted repository.

    Example:

        repository/
            project/
                src/
                package.json

    becomes:

        project/
            src/
            package.json

    This is useful because ZIP files may contain an extra
    top-level folder.
    """

    current_path = repository_path

    while True:
        entries = list(current_path.iterdir())

        directories = [
            entry
            for entry in entries
            if entry.is_dir()
        ]

        files = [
            entry
            for entry in entries
            if entry.is_file()
        ]

        # If the directory contains only one directory
        # and no files, treat that directory as a wrapper.
        if len(directories) == 1 and len(files) == 0:
            current_path = directories[0]
        else:
            break

    return current_path


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate SHA-256 hash of a file.

    The hash helps us quickly determine whether
    a file has changed between two repository versions.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(8192),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def collect_files(repository_path: str) -> dict:
    """
    Collect all files from a repository.

    Returns:
        Dictionary where:
        key   = relative file path
        value = absolute file path
    """

    repository = resolve_repository_root(
        Path(repository_path)
    )

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found: {repository_path}"
        )

    if not repository.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repository_path}"
        )

    files = {}

    for file_path in repository.rglob("*"):

        if file_path.is_file():

            relative_path = file_path.relative_to(
                repository
            )

            files[str(relative_path)] = file_path

    return files


def compare_files(
    original_repository: str,
    modified_repository: str
) -> dict:
    """
    Compare files between original and modified repositories.

    Detects:

    - Added files
    - Deleted files
    - Modified files
    - Unchanged files

    For modified source-code files, it also performs
    line-level comparison.
    """

    # Collect files from both repositories.
    original_files = collect_files(
        original_repository
    )

    modified_files = collect_files(
        modified_repository
    )

    # Get all relative file paths.
    original_paths = set(
        original_files.keys()
    )

    modified_paths = set(
        modified_files.keys()
    )

    # Files existing only in modified repository.
    added_paths = (
        modified_paths - original_paths
    )

    # Files existing only in original repository.
    deleted_paths = (
        original_paths - modified_paths
    )

    # Files existing in both repositories.
    common_paths = (
        original_paths & modified_paths
    )

    changed_paths = set()
    unchanged_paths = set()

    # Compare common files using SHA-256 hash.
    for file_path in common_paths:

        original_hash = calculate_file_hash(
            original_files[file_path]
        )

        modified_hash = calculate_file_hash(
            modified_files[file_path]
        )

        if original_hash != modified_hash:
            changed_paths.add(file_path)

        else:
            unchanged_paths.add(file_path)

    # Perform line-level comparison
    # only for files that actually changed.
    file_changes = {}

    for file_path in changed_paths:

        file_changes[file_path] = compare_lines(
            str(original_files[file_path]),
            str(modified_files[file_path])
        )

    return {
        "addedFiles": sorted(added_paths),
        "deletedFiles": sorted(deleted_paths),
        "modifiedFiles": sorted(changed_paths),
        "unchangedFiles": sorted(unchanged_paths),
        "fileChanges": file_changes
    }