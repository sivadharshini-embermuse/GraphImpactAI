import random

from analyzer.ml_engine.dataset_builder import (
    save_dataset,
    FEATURE_COLUMNS
)


def generate_low_sample():
    """
    Generate a low-impact change sample.
    """

    return {
        "linesAdded": random.randint(1, 5),
        "linesDeleted": random.randint(0, 2),
        "linesChanged": random.randint(0, 3),

        "functionsAdded": 0,
        "functionsDeleted": 0,
        "functionsModified": random.randint(0, 1),

        "classesAdded": 0,
        "classesDeleted": 0,
        "classesModified": 0,

        "importsAdded": 0,
        "importsDeleted": 0,

        "degreeCentrality": random.uniform(0.01, 0.15),
        "betweennessCentrality": random.uniform(0.00, 0.05),
        "pageRank": random.uniform(0.01, 0.08),

        "inDegree": random.randint(0, 2),
        "outDegree": random.randint(0, 2),
        "coupling": random.randint(0, 3)
    }


def generate_medium_sample():
    """
    Generate a medium-impact change sample.
    """

    return {
        "linesAdded": random.randint(10, 25),
        "linesDeleted": random.randint(5, 15),
        "linesChanged": random.randint(8, 20),

        "functionsAdded": random.randint(1, 3),
        "functionsDeleted": random.randint(0, 1),
        "functionsModified": random.randint(2, 5),

        "classesAdded": random.randint(0, 2),
        "classesDeleted": random.randint(0, 1),
        "classesModified": random.randint(1, 3),

        "importsAdded": random.randint(1, 4),
        "importsDeleted": random.randint(0, 2),

        "degreeCentrality": random.uniform(0.25, 0.60),
        "betweennessCentrality": random.uniform(0.10, 0.40),
        "pageRank": random.uniform(0.08, 0.25),

        "inDegree": random.randint(3, 8),
        "outDegree": random.randint(2, 6),
        "coupling": random.randint(5, 14)
    }


def generate_high_sample():
    """
    Generate a high-impact change sample.
    """

    return {
        "linesAdded": random.randint(30, 70),
        "linesDeleted": random.randint(20, 50),
        "linesChanged": random.randint(20, 60),

        "functionsAdded": random.randint(3, 6),
        "functionsDeleted": random.randint(1, 3),
        "functionsModified": random.randint(5, 10),

        "classesAdded": random.randint(1, 3),
        "classesDeleted": random.randint(1, 2),
        "classesModified": random.randint(3, 5),

        "importsAdded": random.randint(2, 6),
        "importsDeleted": random.randint(1, 4),

        "degreeCentrality": random.uniform(0.50, 0.95),
        "betweennessCentrality": random.uniform(0.30, 0.90),
        "pageRank": random.uniform(0.20, 0.60),

        "inDegree": random.randint(8, 20),
        "outDegree": random.randint(5, 12),
        "coupling": random.randint(12, 25)
    }


def add_label(
    features: dict,
    label: str
) -> dict:
    """
    Add the controlled training label.
    """

    row = {}

    for column in FEATURE_COLUMNS:
        row[column] = features.get(
            column,
            0
        )

    row["impactLabel"] = label

    return row


def generate_balanced_dataset(
    samples_per_class: int = 100
) -> list[dict]:

    rows = []

    for _ in range(samples_per_class):

        rows.append(
            add_label(
                generate_low_sample(),
                "Low"
            )
        )

        rows.append(
            add_label(
                generate_medium_sample(),
                "Medium"
            )
        )

        rows.append(
            add_label(
                generate_high_sample(),
                "High"
            )
        )

    random.shuffle(rows)

    return rows


def main():

    rows = generate_balanced_dataset(
        samples_per_class=100
    )

    output_path = (
        "analyzer/data/"
        "training_dataset.csv"
    )

    save_dataset(
        rows,
        output_path
    )

    print(
        "\n========== BALANCED DATASET ==========\n"
    )

    print(
        "Total samples:",
        len(rows)
    )

    labels = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }

    for row in rows:

        labels[
            row["impactLabel"]
        ] += 1

    print(
        "\nClass distribution:"
    )

    for label in [
        "Low",
        "Medium",
        "High"
    ]:

        print(
            f"{label}: {labels[label]}"
        )

    print(
        f"\nDataset saved to: {output_path}"
    )


if __name__ == "__main__":
    main()