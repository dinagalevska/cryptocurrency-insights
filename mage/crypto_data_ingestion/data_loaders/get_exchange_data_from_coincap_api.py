import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load market data from the CoinCap API and return it as a DataFrame.
    """
    url = "https://api.coincap.io/v2/exchanges"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        data_dict = data['data']  # Extract 'data' from the response
        exchanges_df = pd.DataFrame(data_dict)  # Create DataFrame from data
        return exchanges_df  # Return the DataFrame
    else:
        print(f"Failed to fetch data: {response.status_code}")  # Log error
        return pd.DataFrame()  # Return empty DataFrame on error


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'  # Ensure output is defined
    assert isinstance(output, pd.DataFrame), 'Output is not a DataFrame'  # Check output type
    assert not output.empty, 'The output DataFrame is empty'  # Ensure DataFrame is not empty
