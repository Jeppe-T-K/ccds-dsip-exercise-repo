"""Data validation.

Check the ingested raw data before it is used downstream: schema
(column names and types), ranges, missing values, and duplicates.
Fail loudly and early so bad data never reaches model training.
"""


def validate_data(data_path: str) -> bool:
    """Validate the raw data at `data_path`.

    Returns True if all checks pass, raises otherwise.
    """
    raise NotImplementedError
