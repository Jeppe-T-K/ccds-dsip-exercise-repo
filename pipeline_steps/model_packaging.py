"""Model packaging.

Wrap a trained model into a deployable artifact: serialize it together
with its preprocessing, metadata, and dependencies (e.g. a container
image or a serialized pipeline object) so it can be versioned and shipped.
"""


def package_model(model_path: str, artifact_path: str) -> str:
    """Bundle the model at `model_path` into a deployable artifact."""
    raise NotImplementedError
