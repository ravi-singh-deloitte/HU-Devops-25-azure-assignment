from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import BlobContainer
import logging

def setup_storage_account(sub_id, resource_group, account_name, location):
    creds = DefaultAzureCredential()
    storage_client = StorageManagementClient(creds, sub_id)
    logging.info(f"Initiating creation of storage account: {account_name}")
    
    creation_process = storage_client.storage_accounts.begin_create(
        resource_group,
        account_name,
        {
            "location": location,
            "sku": {"name": "Standard_LRS"},
            "kind": "StorageV2"
        }
    )
    creation_result = creation_process.result()
    return creation_result

def setup_blob_container(sub_id, resource_group, account_name, container_name):
    creds = DefaultAzureCredential()
    storage_client = StorageManagementClient(creds, sub_id)
    logging.info(f"Initiating creation of blob container: {container_name}")
    
    storage_client.blob_containers.create(
        resource_group,
        account_name,
        container_name,
        BlobContainer(public_access="None")
    )
