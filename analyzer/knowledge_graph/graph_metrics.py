import networkx as nx


def calculate_degree_centrality(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate degree centrality for every node.
    """

    return nx.degree_centrality(
        graph
    )


def calculate_betweenness_centrality(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate betweenness centrality.

    High value means the node may act as
    an important bridge between other nodes.
    """

    return nx.betweenness_centrality(
        graph
    )


def calculate_pagerank(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate PageRank score for every node.
    """

    return nx.pagerank(
        graph
    )


def calculate_degree_counts(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate incoming and outgoing edge counts.
    """

    result = {}

    for node in graph.nodes():

        result[node] = {
            "inDegree": graph.in_degree(
                node
            ),
            "outDegree": graph.out_degree(
                node
            )
        }

    return result


def calculate_coupling(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate simple coupling as the total number
    of incoming and outgoing relationships.
    """

    result = {}

    for node in graph.nodes():

        result[node] = (
            graph.in_degree(node)
            +
            graph.out_degree(node)
        )

    return result


def calculate_all_metrics(
    graph: nx.DiGraph
) -> dict:
    """
    Calculate all graph metrics for every node.
    """

    degree_centrality = (
        calculate_degree_centrality(
            graph
        )
    )

    betweenness = (
        calculate_betweenness_centrality(
            graph
        )
    )

    pagerank = (
        calculate_pagerank(
            graph
        )
    )

    degree_counts = (
        calculate_degree_counts(
            graph
        )
    )

    coupling = (
        calculate_coupling(
            graph
        )
    )

    metrics = {}

    for node in graph.nodes():

        metrics[node] = {
            "degreeCentrality":
                degree_centrality.get(
                    node,
                    0.0
                ),

            "betweennessCentrality":
                betweenness.get(
                    node,
                    0.0
                ),

            "pageRank":
                pagerank.get(
                    node,
                    0.0
                ),

            "inDegree":
                degree_counts[node][
                    "inDegree"
                ],

            "outDegree":
                degree_counts[node][
                    "outDegree"
                ],

            "coupling":
                coupling.get(
                    node,
                    0
                )
        }

    return metrics







"""
Graph Metrics Module

Calculates graph topology metrics including in-degree, out-degree, depth, and modularity.
"""
