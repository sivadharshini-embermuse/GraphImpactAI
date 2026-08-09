from analyzer.knowledge_graph.complete_graph_analyzer import (
    build_complete_graph
)

from analyzer.knowledge_graph.graph_metrics import (
    calculate_all_metrics
)


def main():

    graph = build_complete_graph(
        "storage/repositories/modified"
    )

    metrics = calculate_all_metrics(
        graph
    )

    print(
        "\n========== GRAPH METRICS ==========\n"
    )

    for node, values in metrics.items():

        print(
            f"\nNode: {node}"
        )

        print(
            f"Degree Centrality: "
            f"{values['degreeCentrality']:.4f}"
        )

        print(
            f"Betweenness: "
            f"{values['betweennessCentrality']:.4f}"
        )

        print(
            f"PageRank: "
            f"{values['pageRank']:.4f}"
        )

        print(
            f"In-Degree: "
            f"{values['inDegree']}"
        )

        print(
            f"Out-Degree: "
            f"{values['outDegree']}"
        )

        print(
            f"Coupling: "
            f"{values['coupling']}"
        )


if __name__ == "__main__":
    main()


