from analyzer.ast.parser_factory import (
    parse_source_file
)

from analyzer.dependencies.dependency_extractor import (
    extract_import_dependencies
)


def main():

    source_code = """
import React from "react";
import UserService from "./services/UserService";
import Database from "../database/Database";
"""

    ast_result = parse_source_file(
        "src/App.js",
        source_code
    )

    dependencies = extract_import_dependencies(
        "src/App.js",
        ast_result
    )

    print(
        "\n========== DEPENDENCY EXTRACTION ==========\n"
    )

    for dependency in dependencies:
        print(dependency)


if __name__ == "__main__":
    main()