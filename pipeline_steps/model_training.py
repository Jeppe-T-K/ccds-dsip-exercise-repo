"""Model training.

Fit one or more candidate models on the prepared training data and
persist the fitted model artifacts (e.g. to `models/`) along with their
training configuration for reproducibility.
"""


def train_model(features_path: str, model_path: str) -> str:
    """Train a model on the features and save it to `model_path`."""
    raise NotImplementedError
