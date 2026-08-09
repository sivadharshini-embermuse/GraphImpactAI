import json
from pathlib import Path

import networkx as nx

from analyzer.knowledge_graph.repository_scanner import (
    scan_repository
)

from analyzer.knowledge_graph.graph_builder import (
    create_repository_graph,
    add_repository_ast_to_graph,
    add_relationship
)


def normalize_import_target(
    current_file: str,
    import_text: str
) -> str | None:
    """
    Convert simple relative imports into
    repository-relative file paths.
    """

    import_text = import_text.strip()

    if not import_text.startswith("."):
        return None

    current_path = Path(
        current_file
    )

    # Remove import syntax around the path.
    import_value = import_text

    if import_value.startswith(
        "import "
    ):
        import_value = import_value[
            len("import "):
        ]

    # Convert ./services/UserService
    # into a normalized path.
    if import_value.startswith("./"):
        import_value = import_value[2:]

    else:
        parent_count = 0

        while import_value.startswith("../"):

            parent_count += 1
            import_value = import_value[3:]

        current_path = current_path.parent

        for _ in range(
            max(parent_count - 1, 0)
        ):
            current_path = current_path.parent

    target = (
        current_path / import_value
    ).as_posix()

    return target


def add_import_relationships(
    graph: nx.DiGraph,
    ast_results: dict
) -> None:
    """
    Add IMPORTS relationships between repository files.
    """

    repository_files = set(
        ast_results.keys()
    )

    for file_path, result in ast_results.items():

        if not result.get(
            "supported",
            False
        ):
            continue

        for import_item in result.get(
            "imports",
            []
        ):

            import_text = import_item.get(
                "text",
                ""
            )

            target = normalize_import_target(
                file_path,
                import_text
            )

            if target is None:
                continue

            # Try common source-code extensions.
            possible_targets = [
                target,
                target + ".js",
                target + ".jsx",
                target + ".ts",
                target + ".tsx",
                target + ".py",
                target + ".java"
            ]

            matched_target = None

            for candidate in possible_targets:

                if candidate in repository_files:
                    matched_target = candidate
                    break

            if matched_target is None:
                continue

            add_relationship(
                graph,
                file_path,
                matched_target,
                "IMPORTS",
                line=import_item.get(
                    "startLine"
                ),
                statement=import_text
            )


def build_complete_graph(
    repository_path: str
) -> nx.DiGraph:
    """
    Build a complete repository knowledge graph.
    """

    ast_results = scan_repository(
        repository_path
    )

    graph = create_repository_graph()

    add_repository_ast_to_graph(
        graph,
        ast_results
    )

    add_import_relationships(
        graph,
        ast_results
    )

    return graph


def save_graph(
    graph: nx.DiGraph,
    output_path: str
) -> None:

    output_file = Path(
        output_path
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    graph_data = nx.node_link_data(
        graph
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            graph_data,
            file,
            indent=4
        )


def main():

    import sys

    if len(sys.argv) != 2:

        print(
            "Usage: python -m "
            "analyzer.graph.complete_graph_analyzer "
            "<repository>"
        )

        return

    repository = sys.argv[1]

    graph = build_complete_graph(
        repository
    )

    output_path = (
        "analyzer/data/outputs/"
        "complete_repository_graph.json"
    )

    save_graph(
        graph,
        output_path
    )

    print(
        "\n========== COMPLETE KNOWLEDGE GRAPH ==========\n"
    )

    print(
        "Nodes:",
        graph.number_of_nodes()
    )

    print(
        "Edges:",
        graph.number_of_edges()
    )

    print(
        f"\nGraph saved to: {output_path}"
    )


if __name__ == "__main__":
    main()