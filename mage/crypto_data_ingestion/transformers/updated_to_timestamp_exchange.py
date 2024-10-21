if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    """
    Transform the input data by creating a 'timestamp' column from the 'updated' column.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        DataFrame with a new 'timestamp' column.
    """
    # Ensure 'updated' column exists
    if 'updated' in data.columns:
        # Convert 'updated' from milliseconds to datetime
        data['timestamp'] = pd.to_datetime(data['updated'], unit='ms')

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert 'timestamp' in output.columns, "The 'timestamp' column is missing"
    assert pd.api.types.is_datetime64_any_dtype(output['timestamp']), "The 'timestamp' column is not in datetime format"
