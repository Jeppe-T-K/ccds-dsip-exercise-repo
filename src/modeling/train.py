from pathlib import Path

import joblib
from loguru import logger
import pandas as pd
from sklearn.linear_model import LogisticRegression
import typer

from src.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    features_path: Path = PROCESSED_DATA_DIR / "train_features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "train_labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
):
    """Train a logistic regression model on the prepared training data."""
    logger.info(f"Training model on {features_path}...")
    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path).squeeze("columns")

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    train_accuracy = model.score(X, y)
    logger.info(f"Training accuracy: {train_accuracy:.3f}")

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    logger.success(f"Model saved to {model_path}")


if __name__ == "__main__":
    app()
