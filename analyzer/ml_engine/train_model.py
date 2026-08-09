import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


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

TARGET_COLUMN = "impactLabel"


def load_dataset(
    dataset_path: str
) -> pd.DataFrame:
    """
    Load the generated training dataset.
    """

    dataset = pd.read_csv(
        dataset_path
    )

    return dataset


def prepare_data(
    dataset: pd.DataFrame
):
    """
    Prepare features and encode impact labels.
    """

    X = dataset[
        FEATURE_COLUMNS
    ]

    y = dataset[
        TARGET_COLUMN
    ]

    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(
        y
    )

    return (
        X,
        y_encoded,
        label_encoder
    )


def train_random_forest(
    X,
    y
):
    """
    Train the Random Forest classifier.
    """

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions,
        output_dict=True
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    return (
        model,
        accuracy,
        report,
        matrix,
        X_test,
        y_test
    )


def save_model(
    model,
    label_encoder,
    model_path: str,
    encoder_path: str
):
    """
    Save the trained Random Forest and label encoder.
    """

    model_file = Path(
        model_path
    )

    encoder_file = Path(
        encoder_path
    )

    model_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        model_file
    )

    joblib.dump(
        label_encoder,
        encoder_file
    )


def save_metrics(
    accuracy,
    report,
    matrix,
    output_path: str
):
    """
    Save model evaluation metrics as JSON.
    """

    output_file = Path(
        output_path
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    metrics = {
        "accuracy": accuracy,
        "classificationReport": report,
        "confusionMatrix": matrix.tolist()
    }

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


def main():

    dataset_path = (
        "analyzer/data/"
        "training_dataset.csv"
    )

    model_path = (
        "analyzer/data/models/"
        "impact_model.pkl"
    )

    encoder_path = (
        "analyzer/data/models/"
        "label_encoder.pkl"
    )

    metrics_path = (
        "analyzer/data/models/"
        "model_metrics.json"
    )

    print(
        "\n========== RANDOM FOREST TRAINING ==========\n"
    )

    dataset = load_dataset(
        dataset_path
    )

    print(
        "Dataset samples:",
        len(dataset)
    )

    X, y, label_encoder = prepare_data(
        dataset
    )

    (
        model,
        accuracy,
        report,
        matrix,
        X_test,
        y_test
    ) = train_random_forest(
        X,
        y
    )

    print(
        f"\nAccuracy: {accuracy:.4f}"
    )

    print(
        "\nClassification Report:\n"
    )

    print(
        classification_report(
            y_test,
            model.predict(X_test),
            target_names=label_encoder.classes_
        )
    )

    print(
        "\nConfusion Matrix:\n"
    )

    print(matrix)

    save_model(
        model,
        label_encoder,
        model_path,
        encoder_path
    )

    save_metrics(
        accuracy,
        report,
        matrix,
        metrics_path
    )

    print(
        "\nModel saved to:",
        model_path
    )

    print(
        "Label encoder saved to:",
        encoder_path
    )

    print(
        "Metrics saved to:",
        metrics_path
    )


if __name__ == "__main__":
    main()