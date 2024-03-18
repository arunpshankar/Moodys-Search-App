from typing import Optional
import os


def convert_to_local_path(gcs_path: str) -> Optional[str]:
    """
    Convert a Google Cloud Storage (GCS) URL to a local file system path.

    This function extracts the filename from a GCS URL and generates a corresponding
    local path where the file can be stored. It ensures that the local directory
    exists and constructs the full local file path.

    Parameters:
    gcs_path (str): The URL of the file in Google Cloud Storage.

    Returns:
    Optional[str]: The local file path corresponding to the GCS URL, or None if the input is not a valid GCS URL.
    """
    # Validate if the GCS path is correctly formatted
    if not gcs_path.startswith("gs://"):
        return None

    # Extract the filename from the GCS URL
    filename = gcs_path.split('/')[-1]

    # Define the local pdf folder path
    local_folder_path = './pdf'

    # Create the folder if it doesn't exist
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    # Create the full local file path
    local_file_path = os.path.join(local_folder_path, filename)

    return local_file_path
