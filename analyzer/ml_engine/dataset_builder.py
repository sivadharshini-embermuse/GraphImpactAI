import csv
from pathlib import Path


FEATURE_COLUMNS = [
    "linesAdded",
    "linesDeleted",
    "linesChanged",
    "functionsAdded",
    "functionsDeleted",
    "functionsModified",
    "classesAdded",
    "classesDeleted",
    "classesModified",
    "importsAdded",
    "importsDeleted",
    "degreeCentrality",
    "betweennessCentrality",
    "pageRank",
    "inDegree",
    "outDegree",
    "coupling"
]


def calculate_impact_score(
    features: dict
) -> float:
    """
    Calculate a deterministic impact score
    from measurable code-change and graph features.

    This is used only to create initial training labels.
    """

    score = 0.0

    # Code change magnitude
    score += min(
        features["linesAdded"] / 50,
        1.0
    ) * 0.10

    score += min(
        features["linesDeleted"] / 50,
        1.0
    ) * 0.10

    score += min(
        features["linesChanged"] / 50,
        1.0
    ) * 0.10

    # Structural changes
    score += min(
        features["functionsModified"] / 10,
        1.0
    ) * 0.15

    score += min(
        features["classesModified"] / 5,
        1.0
    ) * 0.15

    score += min(
        features["functionsAdded"] / 10,
        1.0
    ) * 0.05

    score += min(
        features["classesAdded"] / 5,
        1.0
    ) * 0.05

    # Dependency changes
    score += min(
        features["importsAdded"] / 10,
        1.0
    ) * 0.05

    score += min(
        features["importsDeleted"] / 10,
        1.0
    ) * 0.05

    # Graph importance
    score += min(
        features["degreeCentrality"],
        1.0
    ) * 0.05

    score += min(
        features["betweennessCentrality"],
        1.0
    ) * 0.05

    score += min(
        features["pageRank"],
        1.0
    ) * 0.05

    # Coupling
    score += min(
        features["coupling"] / 20,
        1.0
    ) * 0.10

    return round(
        min(score, 1.0),
        4
    )


def classify_impact(
    score: float
) -> str:
    """
    Convert continuous impact score into
    Low / Medium / High class.
    """

    if score < 0.40:
        return "Low"

    if score < 0.70:
        return "Medium"

    return "High"


def build_training_row(
    features: dict
) -> dict:
    """
    Create one labeled training example.
    """

    score = calculate_impact_score(
        features
    )

    label = classify_impact(
        score
    )

    row = {}

    for column in FEATURE_COLUMNS:
        row[column] = features.get(
            column,
            0
        )

    row["impactScore"] = score
    row["impactLabel"] = label

    return row


def save_dataset(
    rows: list[dict],
    output_path: str
) -> None:
    """
    Save training rows as CSV.
    """

    output_file = Path(
        output_path
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    columns = (
        FEATURE_COLUMNS
        + [
            "impactScore",
            "impactLabel"
        ]
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()

        writer.writerows(rows)