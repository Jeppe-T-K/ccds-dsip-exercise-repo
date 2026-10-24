from pathlib import Path

from loguru import logger
import pandas as pd
from sklearn.model_selection import train_test_split
import typer

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


FEATURE_COLUMNS = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm",
]


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "iris.csv",
    output_dir: Path = PROCESSED_DATA_DIR,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Encode labels and split the raw data into train/test feature and label files."""
    logger.info(f"Generating features from {input_path}...")
    df = pd.read_csv(input_path)

    missing = [c for c in FEATURE_COLUMNS + ["species"] if c not in df.columns]
    if missing:
        raise ValueError(f"Input data is missing expected columns: {missing}")

    X = df[FEATURE_COLUMNS]
    y = df["species"].astype("category")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    X_train.to_csv(output_dir / "train_features.csv", index=False)
    y_train.to_csv(output_dir / "train_labels.csv", index=False)
    X_test.to_csv(output_dir / "test_features.csv", index=False)
    y_test.to_csv(output_dir / "test_labels.csv", index=False)

    logger.success(
        f"Split done: {len(X_train)} train / {len(X_test)} test rows " f"written to {output_dir}"
    )


if __name__ == "__main__":
    app()
