import os
from azure.storage.blob import BlobServiceClient

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Retrieve environment variables
account_name = os.getenv('STORAGE_ACCOUNT_NAME')
account_key = os.getenv('STORAGE_ACCOUNT_KEY')
container_a = 'container-a'
container_b = 'container-b'
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

def transfer_blob():
    # Get the blob clients for both containers
    container_a_client = blob_service_client.get_container_client(container_a)
    container_b_client = blob_service_client.get_container_client(container_b)

    # Download the file from container-a
    blob_a = container_a_client.get_blob_client('file1.txt')
    file_data = blob_a.download_blob().readall()

    # Upload the file to container-b
    blob_b = container_b_client.get_blob_client('file1.txt')
    blob_b.upload_blob(file_data, overwrite=True)

if __name__ == "__main__":
    transfer_blob()
