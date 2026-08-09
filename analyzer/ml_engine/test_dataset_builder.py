from analyzer.ml_engine.dataset_builder import (
    build_training_row,
    save_dataset
)


def main():

    features = {
        "linesAdded": 8,
        "linesDeleted": 2,
        "linesChanged": 4,

        "functionsAdded": 1,
        "functionsDeleted": 0,
        "functionsModified": 2,

        "classesAdded": 0,
        "classesDeleted": 0,
        "classesModified": 1,

        "importsAdded": 1,
        "importsDeleted": 0,

        "degreeCentrality": 0.42,
        "betweennessCentrality": 0.31,
        "pageRank": 0.18,

        "inDegree": 4,
        "outDegree": 2,
        "coupling": 6
    }

    row = build_training_row(
        features
    )

    print(
        "\n========== TRAINING SAMPLE ==========\n"
    )

    for key, value in row.items():
        print(
            f"{key}: {value}"
        )

    save_dataset(
        [row],
        "analyzer/data/training_dataset.csv"
    )

    print(
        "\nDataset saved successfully."
    )


if __name__ == "__main__":
    main()