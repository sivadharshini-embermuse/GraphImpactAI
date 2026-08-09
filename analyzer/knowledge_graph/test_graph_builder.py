import networkx as nx

from analyzer.knowledge_graph.graph_builder import (
    create_repository_graph,
    add_file_node,
    add_entity_node,
    add_relationship
)


def main():

    graph = create_repository_graph()

    # File nodes
    add_file_node(
        graph,
        "src/App.js",
        "javascript"
    )

    add_file_node(
        graph,
        "src/UserService.js",
        "javascript"
    )

    # Function node
    add_entity_node(
        graph,
        "src/App.js::function::calculatePrice",
        "function",
        "calculatePrice",
        "src/App.js",
        10,
        15
    )

    # Relationships
    add_relationship(
        graph,
        "src/App.js",
        "src/App.js::function::calculatePrice",
        "CONTAINS"
    )

    add_relationship(
        graph,
        "src/App.js",
        "src/UserService.js",
        "IMPORTS"
    )

    print(
        "\n========== KNOWLEDGE GRAPH ==========\n"
    )

    print(
        "Nodes:"
    )

    for node, data in graph.nodes(data=True):
        print(
            node,
            "->",
            data
        )

    print(
        "\nEdges:"
    )

    for source, target, data in graph.edges(data=True):
        print(
            source,
            "--",
            data["type"],
            "-->",
            target
        )

    print(
        "\nTotal nodes:",
        graph.number_of_nodes()
    )

    print(
        "Total edges:",
        graph.number_of_edges()
    )


if __name__ == "__main__":
    main()