from typing import Any


def count_entities(
    entity_group: dict,
    group_name: str
) -> int:
    """
    Count entities belonging to a specific
    AST change category.
    """

    return len(
        entity_group.get(
            group_name,
            []
        )
    )


def build_ast_features(
    ast_result: dict
) -> dict:
    """
    Extract numerical features from AST
    structural comparison results.
    """

    functions = ast_result.get(
        "functions",
        {}
    )

    classes = ast_result.get(
        "classes",
        {}
    )

    imports = ast_result.get(
        "imports",
        {}
    )

    return {
        "functionsAdded":
            count_entities(
                functions,
                "added"
            ),

        "functionsDeleted":
            count_entities(
                functions,
                "deleted"
            ),

        "functionsModified":
            count_entities(
                functions,
                "modified"
            ),

        "classesAdded":
            count_entities(
                classes,
                "added"
            ),

        "classesDeleted":
            count_entities(
                classes,
                "deleted"
            ),

        "classesModified":
            count_entities(
                classes,
                "modified"
            ),

        "importsAdded":
            len(
                imports.get(
                    "added",
                    []
                )
            ),

        "importsDeleted":
            len(
                imports.get(
                    "deleted",
                    []
                )
            )
    }


def build_change_features(
    line_change_result: dict
) -> dict:
    """
    Extract numerical features from line-level
    comparison results.
    """

    return {
        "linesAdded":
            line_change_result.get(
                "linesAdded",
                0
            ),

        "linesDeleted":
            line_change_result.get(
                "linesDeleted",
                0
            ),

        "linesChanged":
            line_change_result.get(
                "linesChanged",
                0
            )
    }


def build_graph_features(
    graph_metrics: dict
) -> dict:
    """
    Convert graph metrics into ML features.
    """

    return {
        "degreeCentrality":
            graph_metrics.get(
                "degreeCentrality",
                0.0
            ),

        "betweennessCentrality":
            graph_metrics.get(
                "betweennessCentrality",
                0.0
            ),

        "pageRank":
            graph_metrics.get(
                "pageRank",
                0.0
            ),

        "inDegree":
            graph_metrics.get(
                "inDegree",
                0
            ),

        "outDegree":
            graph_metrics.get(
                "outDegree",
                0
            ),

        "coupling":
            graph_metrics.get(
                "coupling",
                0
            )
    }


def build_feature_vector(
    file_path: str,
    line_change_result: dict,
    ast_result: dict,
    graph_metrics: dict
) -> dict:
    """
    Combine line, AST and graph information
    into a single feature vector.
    """

    features = {
        "filePath": file_path
    }

    features.update(
        build_change_features(
            line_change_result
        )
    )

    features.update(
        build_ast_features(
            ast_result
        )
    )

    features.update(
        build_graph_features(
            graph_metrics
        )
    )

    return features







"""
Feature Builder Module

Aggregates code diffs, AST metrics, and graph features into a unified dataset matrix.
"""
