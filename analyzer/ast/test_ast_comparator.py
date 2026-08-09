from analyzer.ast.ast_comparator import (
    compare_ast_sources
)


def main():

    original_python = """
def calculate_price():
    return 100


def get_user():
    return "Sivu"
"""

    modified_python = """
def calculate_price():
    return 150


def get_user():
    return "Sivu"


def apply_discount():
    return 10
"""

    result = compare_ast_sources(
        "app.py",
        original_python,
        modified_python
    )

    print("\n========== AST STRUCTURAL COMPARISON ==========\n")

    print(result)


if __name__ == "__main__":
    main()