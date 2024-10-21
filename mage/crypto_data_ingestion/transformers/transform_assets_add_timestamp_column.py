import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Args:
        data: The output from the upstream parent block (assumed to be a DataFrame).
        args: The output from any additional upstream blocks (if applicable).

    Returns:
        A transformed DataFrame with the 'time' column converted to a timestamp.
    """
    # Check if 'data' is a DataFrame
    if isinstance(data, pd.DataFrame):
        # Convert the 'time' column from milliseconds since epoch to a timestamp
        data['timestamp'] = pd.to_datetime(data['time'], unit='ms')
        
        # Optionally drop the original 'time' column if it's no longer needed
        # data.drop(columns=['time'], inplace=True)  # Uncomment if you want to drop
        
        return data
    else:
        raise ValueError("Expected data to be a DataFrame")


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert 'timestamp' in output.columns, "The output DataFrame does not have a 'timestamp' column"
    assert pd.api.types.is_datetime64_any_dtype(output['timestamp']), "The 'timestamp' column is not in datetime format"
