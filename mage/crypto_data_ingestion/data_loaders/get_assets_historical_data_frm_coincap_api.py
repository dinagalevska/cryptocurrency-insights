import pandas as pd
import requests
from datetime import datetime, timedelta

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def generate_timestamps_for_period(days: int) -> tuple[int, int]:
    """
    Generates start and end timestamps in milliseconds for a given period in days.
    """
    start_timestamp = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    end_timestamp = int(datetime.now().timestamp() * 1000)
    return start_timestamp, end_timestamp

def fetch_asset_ids() -> list[str]:
    """
    Retrieves a list of asset IDs from the CoinCap API.
    """
    response = requests.get(url="https://api.coincap.io/v2/assets").json()
    return [asset["id"] for asset in response["data"]]

def retrieve_asset_history(days: int) -> dict[str, list]:
    """
    Collects historical data for all assets for a specified number of days.
    """
    start_timestamp, end_timestamp = generate_timestamps_for_period(days)
    asset_ids = fetch_asset_ids()
    data_columns_initialized = False
    historical_data = {}

    # Loop through each asset ID to fetch its historical data
    for asset_id in asset_ids:
        response = requests.get(
            url=f"https://api.coincap.io/v2/assets/{asset_id}/history",
            params={
                "interval": "h1",  # Fetching data with a 1-hour interval
                "start": start_timestamp,
                "end": end_timestamp,
            },
        )

        # Verify the response is successful
        if response.status_code == 200:
            response_json = response.json()
            # Check if the response contains data
            if "data" in response_json and response_json["data"]:
                if not data_columns_initialized:
                    # Initialize columns based on the first response's keys
                    columns = list(response_json["data"][0].keys()) + ["id"]
                    historical_data = {k: [] for k in columns}
                    data_columns_initialized = True

                # Store the data into the dictionary
                for entry in response_json["data"]:
                    for key in entry:
                        historical_data[key].append(entry[key])
                    historical_data["id"].append(asset_id)
            else:
                print(f"No data available for asset: {asset_id}")
        else:
            print(f"Failed to fetch data for asset {asset_id}: Status Code {response.status_code}")

    return historical_data

@data_loader
def load_asset_data(*args, **kwargs):
    """
    Loads historical asset data from the CoinCap API based on a specified number of days.
    """
    days = kwargs['days']  # Days parameter is required

    # Retrieve the asset history data and convert it to a DataFrame
    historical_data = retrieve_asset_history(days)
    data_frame = pd.DataFrame(historical_data)

    # Return only the DataFrame
    return data_frame

@test
def validate_output(output, *args) -> None:
    """
    Validates the output of the data loader block.
    """
    assert output is not None, 'The output is undefined'
    assert not output.empty, 'The output DataFrame is empty'
    assert 'id' in output.columns, 'The DataFrame must include an "id" column for asset IDs'
