from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from sklearn.datasets import load_iris
import typer

from src.config import RAW_DATA_DIR

load_dotenv()

app = typer.Typer()


IRIS_COLUMNS = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm",
    "species",
]


@app.command()
def main(
    output_path: Path = RAW_DATA_DIR / "iris.csv",
):
    """Load the iris dataset and persist it as raw CSV."""
    logger.info("Loading iris dataset...")
    bunch = load_iris(as_frame=True)
    df = bunch.frame.rename(
        columns={
            "sepal length (cm)": IRIS_COLUMNS[0],
            "sepal width (cm)": IRIS_COLUMNS[1],
            "petal length (cm)": IRIS_COLUMNS[2],
            "petal width (cm)": IRIS_COLUMNS[3],
            "target": "species",
        }
    )
    df["species"] = df["species"].map({i: name for i, name in enumerate(bunch.target_names)})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Saved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    app()
