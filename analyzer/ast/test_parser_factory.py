from analyzer.ast.parser_factory import (
    detect_language,
    parse_source_file
)


def main():

    test_files = [
        "app.py",
        "app.js",
        "app.ts",
        "UserService.java",
        "image.png"
    ]

    print("\n========== LANGUAGE DETECTION ==========\n")

    for file_path in test_files:

        language = detect_language(file_path)

        print(
            f"{file_path} -> {language}"
        )

    python_result = parse_source_file(
        "app.py",
        """
def hello():
    return "Hello"
"""
    )

    print("\n========== PYTHON ==========")
    print(python_result)

    javascript_result = parse_source_file(
        "app.js",
        """
function hello() {
    return "Hello";
}
"""
    )

    print("\n========== JAVASCRIPT ==========")
    print(javascript_result)


if __name__ == "__main__":
    main()