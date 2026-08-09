from analyzer.feature_extraction.feature_builder import (
    build_feature_vector
)


def main():

    line_changes = {
        "linesAdded": 5,
        "linesDeleted": 2,
        "linesChanged": 3
    }

    ast_result = {
        "functions": {
            "added": [
                {"name": "apply_discount"}
            ],
            "deleted": [],
            "modified": [
                {"name": "calculate_price"}
            ],
            "unchanged": [
                "get_user"
            ]
        },

        "classes": {
            "added": [],
            "deleted": [],
            "modified": [
                {"name": "OrderService"}
            ],
            "unchanged": []
        },

        "imports": {
            "added": [
                "import Database"
            ],
            "deleted": []
        }
    }

    graph_metrics = {
        "degreeCentrality": 0.42,
        "betweennessCentrality": 0.31,
        "pageRank": 0.18,
        "inDegree": 4,
        "outDegree": 2,
        "coupling": 6
    }

    features = build_feature_vector(
        "src/App.js",
        line_changes,
        ast_result,
        graph_metrics
    )

    print(
        "\n========== ML FEATURE VECTOR ==========\n"
    )

    for name, value in features.items():

        print(
            f"{name}: {value}"
        )


if __name__ == "__main__":
    main()