from pathlib import Path

from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import typer

from src.config import FIGURES_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "iris.csv",
    output_path: Path = FIGURES_DIR / "iris_scatter.png",
):
    """Plot petal length vs petal width, colored by species."""
    logger.info(f"Generating plot from {input_path}...")
    df = pd.read_csv(input_path)

    fig, ax = plt.subplots(figsize=(8, 6))
    for species, group in df.groupby("species"):
        ax.scatter(
            group["petal_length_cm"],
            group["petal_width_cm"],
            label=species,
            alpha=0.7,
        )
    ax.set_xlabel("Petal length (cm)")
    ax.set_ylabel("Petal width (cm)")
    ax.set_title("Iris petals by species")
    ax.legend(title="Species")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.success(f"Plot saved to {output_path}")


if __name__ == "__main__":
    app()
