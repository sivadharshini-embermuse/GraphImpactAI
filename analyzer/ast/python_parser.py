from tree_sitter_language_pack import get_parser


def parse_python(source_code: str) -> dict:
    """
    Parse Python source code using Tree-sitter.

    Returns structured AST information including:
    - Functions
    - Classes
    - Imports
    - Syntax errors
    """

    parser = get_parser("python")

    source_bytes = source_code.encode("utf-8")

    tree = parser.parse(source_bytes)

    root_node = tree.root_node

    functions = []
    classes = []
    imports = []
    errors = []

    def walk(node):
        """
        Recursively traverse the AST.
        """

        node_type = node.type

        if node_type == "function_definition":
            name_node = node.child_by_field_name("name")

            functions.append({
                "name": (
                    name_node.text.decode("utf-8")
                    if name_node
                    else "anonymous"
                ),
                "startLine": node.start_point[0] + 1,
                "endLine": node.end_point[0] + 1
            })

        elif node_type == "class_definition":
            name_node = node.child_by_field_name("name")

            classes.append({
                "name": (
                    name_node.text.decode("utf-8")
                    if name_node
                    else "anonymous"
                ),
                "startLine": node.start_point[0] + 1,
                "endLine": node.end_point[0] + 1
            })

        elif node_type in {
            "import_statement",
            "import_from_statement"
        }:
            imports.append({
                "type": node_type,
                "text": node.text.decode("utf-8"),
                "startLine": node.start_point[0] + 1,
                "endLine": node.end_point[0] + 1
            })

        if node.is_error or node.is_missing:
            errors.append({
                "type": node_type,
                "startLine": node.start_point[0] + 1,
                "endLine": node.end_point[0] + 1
            })

        for child in node.children:
            walk(child)

    walk(root_node)

    return {
        "language": "python",
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "errors": errors
    }



"""
Python AST Parser

Tree-sitter parser for Python source code AST node extraction.
"""
