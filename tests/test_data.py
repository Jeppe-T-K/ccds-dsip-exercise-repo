from pathlib import Path

import pandas as pd

from src import dataset, features
from src.modeling import predict, train


EXPECTED_COLUMNS = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm",
    "species",
]


def test_dataset_creates_raw_csv(tmp_path: Path):
    output_path = tmp_path / "iris.csv"
    dataset.main(output_path=output_path)

    df = pd.read_csv(output_path)
    assert list(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 150
    assert set(df["species"]) == {"setosa", "versicolor", "virginica"}


def test_features_splits_train_test(tmp_path: Path):
    output_dir = tmp_path / "processed"
    features.main(output_dir=output_dir)

    train_X = pd.read_csv(output_dir / "train_features.csv")
    train_y = pd.read_csv(output_dir / "train_labels.csv")
    test_X = pd.read_csv(output_dir / "test_features.csv")
    test_y = pd.read_csv(output_dir / "test_labels.csv")

    assert len(train_X) + len(test_X) == 150
    assert len(train_X) == len(train_y)
    assert len(test_X) == len(test_y)
    assert train_X.columns.tolist() == EXPECTED_COLUMNS[:4]
    assert train_y.columns.tolist() == ["species"]


def test_train_and_predict(tmp_path: Path):
    features.main(output_dir=tmp_path)
    train.main(
        features_path=tmp_path / "train_features.csv",
        labels_path=tmp_path / "train_labels.csv",
        model_path=tmp_path / "model.pkl",
    )
    assert (tmp_path / "model.pkl").exists()

    predict.main(
        features_path=tmp_path / "test_features.csv",
        labels_path=tmp_path / "test_labels.csv",
        model_path=tmp_path / "model.pkl",
        predictions_path=tmp_path / "test_predictions.csv",
        report_path=tmp_path / "metrics.txt",
    )

    predictions = pd.read_csv(tmp_path / "test_predictions.csv")
    test_y = pd.read_csv(tmp_path / "test_labels.csv")
    assert len(predictions) == len(test_y)

    report = (tmp_path / "metrics.txt").read_text()
    assert "Accuracy" in report
    accuracy = float(report.split("Accuracy:")[1].split()[0])
    assert accuracy > 0.8
