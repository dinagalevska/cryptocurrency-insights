if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd  # Import pandas if you haven't already

@transformer
def transform(data, *args, **kwargs):
    """
    Transform the data to add a flag for rates data.

    Args:
        data: The output from the upstream parent block
        args: Additional arguments (if applicable)

    Returns:
        The transformed DataFrame with an added flag column.
    """
    # Check if data is a DataFrame
    if isinstance(data, pd.DataFrame):
        # Add a flag column specific for rates data
        data['flag'] = 'rates'  # Set flag value for all rows
        
        # Optional: You can also perform other transformations here

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert 'flag' in output.columns, 'Flag column is missing'
    assert all(output['flag'] == 'rates'), 'Flag column does not contain the expected value'
