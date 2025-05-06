
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import Site, SiteConfigResource, SiteSourceControl
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
location = os.getenv('APP_SERVICE_PLAN_LOCATION')
app_service_plan_name = os.getenv('APP_SERVICE_PLAN_NAME')
web_app_name = os.getenv('WEB_APP_NAME')
repo_url = os.getenv('REPO_URL')

# Azure credentials and client
credential = DefaultAzureCredential()
client = WebSiteManagementClient(credential, subscription_id)

def create_web_app():
    logger.info("Creating Linux-based Python web app...")

    site_config = {
        "linux_fx_version": "PYTHON|3.9"
    }

    site = Site(
        location=location,
        server_farm_id=app_service_plan_name,
        site_config=site_config
    )

    # Create web app
    webapp = client.web_apps.begin_create_or_update(
        resource_group,
        web_app_name,
        site
    ).result()

    logger.info(f"Web app '{webapp.name}' created successfully.")

    # Deploy source code from GitHub
    logger.info("Setting GitHub repo as deployment source...")

    source_control = SiteSourceControl(
        location=location,
        repo_url=repo_url,
        branch="master",
        is_manual_integration=True,
        is_mercurial=False
    )

    client.web_apps.begin_create_or_update_source_control(
        resource_group,
        web_app_name,
        source_control
    ).result()

    logger.info(f"Deployment source set to GitHub repo: {repo_url}")

if __name__ == "__main__":
    create_web_app()

