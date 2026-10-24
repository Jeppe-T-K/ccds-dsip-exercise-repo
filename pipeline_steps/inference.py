"""Inference/serving.

Expose the packaged model for predictions: batch scoring against
stored data, or a live service (e.g. a REST API) that loads the model
artifact once and serves low-latency predictions.
"""


def predict(artifact_path: str, input_data) -> object:
    """Load the packaged model and return predictions for `input_data`."""
    raise NotImplementedError
