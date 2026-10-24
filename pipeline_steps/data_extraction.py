"""Data extraction/ingestion.

Fetch raw data from its source (database, API, files, etc.) and store it
in `data/raw/` without any transformation, so the rest of the pipeline
works on a stable, immutable copy.
"""


def extract_data(source: str, output_path: str) -> str:
    """Read data from `source` and persist it to `output_path`.

    Returns the path of the ingested raw data.
    """
    raise NotImplementedError
