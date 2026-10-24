"""Data preparation.

Turn validated raw data into model-ready features: cleaning,
imputation, encoding, feature engineering, and train/test splitting.
The output is persisted to `data/processed/`.
"""


def prepare_data(data_path: str, output_path: str) -> str:
    """Transform raw data at `data_path` into features at `output_path`."""
    raise NotImplementedError
