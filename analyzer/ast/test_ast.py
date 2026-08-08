from analyzer.ast.python_parser import parse_python
from analyzer.ast.javascript_parser import parse_javascript


def main():

    python_code = """
import os

class UserService:

    def get_user(self):
        return "Sivu"

def calculate_price():
    return 100
"""

    javascript_code = """
import React from "react";

class App {
    render() {
        return "Hello";
    }
}

function calculatePrice() {
    return 100;
}
"""

    python_result = parse_python(
        python_code
    )

    javascript_result = parse_javascript(
        javascript_code
    )

    print("\n========== PYTHON AST ==========")

    print(python_result)

    print("\n========== JAVASCRIPT AST ==========")

    print(javascript_result)


if __name__ == "__main__":
    main()