import os
import logging
from azure.identity import AzureCliCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import SkuDescription, AppServicePlan
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Read values from .env
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
app_service_plan_name = os.getenv('APP_SERVICE_PLAN_NAME')
location = os.getenv('APP_SERVICE_PLAN_LOCATION')

# Validate inputsX
if not all([subscription_id, resource_group, app_service_plan_name, location]):
    raise EnvironmentError("One or more required environment variables are missing.")

# Authenticate using Azure CLI (az login)
credential = AzureCliCredential()

# Initialize client
client = WebSiteManagementClient(credential, subscription_id)

# Create the App Service Plan
def create_app_service_plan():
    logger.info("Creating App Service Plan using Azure CLI credentials...")

    sku = SkuDescription(name="B1", tier="Basic", size="B1", family="B", capacity=1)
    app_service_plan = AppServicePlan(
        location=location,
        sku=sku,
        reserved=True,  # Linux-based
        kind="linux"
    )

    plan = client.app_service_plans.begin_create_or_update(
        resource_group,
        app_service_plan_name,
        app_service_plan
    ).result()

    logger.info(f"App Service Plan '{plan.name}' created successfully in region '{plan.location}'")
    return plan

if __name__ == "__main__":
    create_app_service_plan()
