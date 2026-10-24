from pathlib import Path

import joblib
from loguru import logger
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import typer

from src.config import MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR

app = typer.Typer()


@app.command()
def main(
    features_path: Path = PROCESSED_DATA_DIR / "test_features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "test_labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv",
    report_path: Path = REPORTS_DIR / "metrics.txt",
):
    """Run inference on the held-out test set and report metrics."""
    logger.info(f"Loading model from {model_path}...")
    model = joblib.load(model_path)

    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path).squeeze("columns")

    logger.info("Predicting on test set...")
    predictions = model.predict(X)

    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"prediction": predictions}).to_csv(predictions_path, index=False)

    accuracy = accuracy_score(y, predictions)
    report = classification_report(y, predictions)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(f"Accuracy: {accuracy:.3f}\n\n{report}")

    logger.info(f"Test accuracy: {accuracy:.3f}")
    logger.success(f"Predictions saved to {predictions_path}")
    logger.success(f"Metrics saved to {report_path}")


if __name__ == "__main__":
    app()
