"""Model evaluation.

Score a trained model on held-out data using agreed metrics, and
persist the results (numbers and figures) to `reports/` so runs can be
compared before any model is promoted.
"""


def evaluate_model(model_path: str, test_data_path: str, report_path: str) -> dict:
    """Evaluate the model and write metrics/plots to `report_path`."""
    raise NotImplementedError
