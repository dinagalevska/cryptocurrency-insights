if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import logging
from google.cloud import storage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@custom
def transform_custom(*args, **kwargs):
    """
    This function tests the connection to Google Cloud Storage by listing available buckets.
    """
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        
        if buckets:
            logger.info("Connected successfully! Available buckets:")
            bucket_details = []
            for bucket in buckets:
                details = {
                    "name": bucket.name,
                    "location": bucket.location,
                    "created": bucket.time_created
                }
                logger.info(f"Bucket Details: {details}")
                bucket_details.append(details)
        else:
            logger.info("Connected successfully, but no buckets found.")

        return {"buckets": bucket_details}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}

@test
def test_output(output, *args) -> None:
    """
    Tests the output of the transform_custom block.
    """
    if output is None:
        raise ValueError('The output is undefined')
    if not isinstance(output, dict):
        raise TypeError('The output should be a dictionary')
    if 'buckets' not in output:
        raise KeyError('The output dictionary should contain a "buckets" key')

    # If there are buckets, you can also log them
    if output['buckets']:
        logger.info(f"Test passed: Found buckets: {output['buckets']}")
    else:
        logger.warning("Test passed, but no buckets found.")
