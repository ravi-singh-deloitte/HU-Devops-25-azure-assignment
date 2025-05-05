import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
from dotenv import load_dotenv
from modules.storage  import setup_storage_account, setup_blob_container


load_dotenv()
logging.basicConfig(level=logging.INFO)

subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("RESOURCE_GROUP")
location = os.getenv("LOCATION")
storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")
container_name = os.getenv("CONTAINER_NAME")

setup_storage_account(subscription_id, resource_group, storage_account_name, location)
setup_blob_container(subscription_id, resource_group, storage_account_name, container_name)
