from pathlib import Path

from .python_parser import parse_python
from .javascript_parser import parse_javascript
from .typescript_parser import parse_typescript
from .java_parser import parse_java


SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
}


def detect_language(file_path: str) -> str | None:
    """
    Detect the programming language from the file extension.
    """

    extension = Path(file_path).suffix.lower()

    return SUPPORTED_LANGUAGES.get(extension)


def parse_source_file(
    file_path: str,
    source_code: str
) -> dict:
    """
    Select the correct AST parser based on the file extension.
    """

    language = detect_language(file_path)

    if language is None:
        return {
            "language": None,
            "supported": False,
            "message": "Unsupported programming language.",
            "functions": [],
            "classes": [],
            "imports": [],
            "errors": []
        }

    if language == "python":
        result = parse_python(source_code)

    elif language == "javascript":
        result = parse_javascript(source_code)

    elif language == "typescript":
        result = parse_typescript(source_code)

    elif language == "java":
        result = parse_java(source_code)

    else:
        raise ValueError(
            f"No parser registered for language: {language}"
        )

    result["supported"] = True

    return result


"""
Parser Factory

Factory pattern implementation to dynamically instantiate language-specific AST parsers.
"""
