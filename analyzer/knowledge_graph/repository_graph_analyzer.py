import json
from pathlib import Path

import networkx as nx

from analyzer.ast.repository_ast_analyzer import (
    analyze_changed_files
)

from analyzer.knowledge_graph.graph_builder import (
    create_repository_graph,
    add_file_node,
    add_entity_node,
    add_relationship
)


def add_ast_entities_to_graph(
    graph: nx.DiGraph,
    file_path: str,
    ast_result: dict
) -> None:
    """
    Add functions and classes extracted from AST
    as nodes in the knowledge graph.
    """

    if not ast_result.get("supported", False):
        return

    language = ast_result.get(
        "language"
    )

    # Add file node.
    add_file_node(
        graph,
        file_path,
        language
    )

    # -------------------------
    # Functions
    # -------------------------

    functions = ast_result.get(
        "functions",
        {}
    )

    for group_name in [
        "added",
        "deleted",
        "modified",
        "unchanged"
    ]:

        for function in functions.get(
            group_name,
            []
        ):

            if isinstance(function, str):

                name = function
                start_line = None
                end_line = None

            else:

                name = function.get(
                    "name",
                    "anonymous"
                )

                start_line = function.get(
                    "startLine"
                )

                end_line = function.get(
                    "endLine"
                )

            entity_id = (
                f"{file_path}::"
                f"function::"
                f"{name}"
            )

            add_entity_node(
                graph,
                entity_id,
                "function",
                name,
                file_path,
                start_line,
                end_line
            )

            add_relationship(
                graph,
                file_path,
                entity_id,
                "CONTAINS"
            )

    # -------------------------
    # Classes
    # -------------------------

    classes = ast_result.get(
        "classes",
        {}
    )

    for group_name in [
        "added",
        "deleted",
        "modified",
        "unchanged"
    ]:

        for class_entity in classes.get(
            group_name,
            []
        ):

            if isinstance(
                class_entity,
                str
            ):

                name = class_entity
                start_line = None
                end_line = None

            else:

                name = class_entity.get(
                    "name",
                    "anonymous"
                )

                start_line = class_entity.get(
                    "startLine"
                )

                end_line = class_entity.get(
                    "endLine"
                )

            entity_id = (
                f"{file_path}::"
                f"class::"
                f"{name}"
            )

            add_entity_node(
                graph,
                entity_id,
                "class",
                name,
                file_path,
                start_line,
                end_line
            )

            add_relationship(
                graph,
                file_path,
                entity_id,
                "CONTAINS"
            )


def build_repository_graph(
    original_repository: str,
    modified_repository: str
) -> nx.DiGraph:
    """
    Build a knowledge graph from the modified
    source-code repository and its AST changes.
    """

    ast_analysis = analyze_changed_files(
        original_repository,
        modified_repository
    )

    graph = create_repository_graph()

    for file_path, ast_result in ast_analysis[
        "results"
    ].items():

        add_ast_entities_to_graph(
            graph,
            file_path,
            ast_result
        )

    return graph


def save_graph(
    graph: nx.DiGraph,
    output_path: str
) -> None:
    """
    Save the graph as JSON node-link data.
    """

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

    if len(sys.argv) != 3:

        print(
            "Usage: python -m "
            "analyzer.graph.repository_graph_analyzer "
            "<original_repository> "
            "<modified_repository>"
        )

        return

    original_repository = sys.argv[1]
    modified_repository = sys.argv[2]

    graph = build_repository_graph(
        original_repository,
        modified_repository
    )

    output_path = (
        "analyzer/data/outputs/"
        "repository_graph.json"
    )

    save_graph(
        graph,
        output_path
    )

    print(
        "\n========== REPOSITORY KNOWLEDGE GRAPH ==========\n"
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