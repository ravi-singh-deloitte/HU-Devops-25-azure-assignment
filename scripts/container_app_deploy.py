
import os
import logging
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.appcontainers import ContainerAppsAPIClient
from azure.mgmt.appcontainers.models import (
    ManagedEnvironment,
    ContainerApp,
    Template,
    Container,
    RegistryCredentials,
    Configuration,
    Secret
)

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variables
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
LOCATION = os.getenv("LOCATION")
ACR_NAME = os.getenv("ACR_NAME")
CONTAINER_ENV_NAME = os.getenv("CONTAINER_ENV_NAME")
CONTAINER_APP_NAME = os.getenv("CONTAINER_APP_NAME")
DOCKER_IMAGE_REPO = os.getenv("DOCKER_IMAGE_REPO")
DOCKER_IMAGE_TAG = os.getenv("DOCKER_IMAGE_TAG")
ACR_USER_NAME = os.getenv("ACR_USER_NAME")
ACR_PASSWORD = os.getenv("ACR_PASSWORD")

# Setup Azure credentials and Container Apps client
credential = DefaultAzureCredential()
container_client = ContainerAppsAPIClient(credential, SUBSCRIPTION_ID)

def create_managed_env():
    try:
        logger.info(f"Checking if Managed Environment '{CONTAINER_ENV_NAME}' exists...")
        container_client.managed_environments.get(RESOURCE_GROUP, CONTAINER_ENV_NAME)
        logger.info("Managed Environment already exists.")
    except ResourceNotFoundError:
        logger.info("Managed Environment not found. Creating it now...")
        poller = container_client.managed_environments.begin_create_or_update(
            resource_group_name=RESOURCE_GROUP,
            environment_name=CONTAINER_ENV_NAME,
            environment_envelope=ManagedEnvironment(
                location=LOCATION,
                tags={
                    "HU_BATCH": "HU-DevOps-25",
                    "USER_NAME": "rsingh95"
                }
            )
        )
        poller.result()
        logger.info("Managed Environment created successfully.")

def deploy_container_app():
    logger.info(f"Deploying Container App: {CONTAINER_APP_NAME}")

    image = f"{ACR_NAME}.azurecr.io/{DOCKER_IMAGE_REPO}:{DOCKER_IMAGE_TAG}"

    registry_credentials = RegistryCredentials(
        server=f"{ACR_NAME}.azurecr.io",
        username=ACR_USER_NAME,
        password_secret_ref="acrpassword"
    )

    container_app = ContainerApp(
        location=LOCATION,
        configuration=Configuration(
            ingress={
                "external": True,
                "target_port": 80,
            },
            registries=[registry_credentials],
            secrets=[
                Secret(name="acrpassword", value=ACR_PASSWORD)
            ]
        ),
        template=Template(
            containers=[
                Container(
                    name="nginx",
                    image=image,
                    resources={"cpu": 0.25, "memory": "0.5Gi"},
                )
            ]
        ),
        managed_environment_id=(
            f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/"
            f"providers/Microsoft.App/managedEnvironments/{CONTAINER_ENV_NAME}"
        ),
        tags={
            "HU_BATCH": "HU-DevOps-25",
            "USER_NAME": "rsingh95"
        }
    )

    poller = container_client.container_apps.begin_create_or_update(
        resource_group_name=RESOURCE_GROUP,
        container_app_name=CONTAINER_APP_NAME,
        container_app_envelope=container_app
    )
    
    result = poller.result()

    container_app_details = container_client.container_apps.get(
        resource_group_name=RESOURCE_GROUP,
        container_app_name=CONTAINER_APP_NAME
    )

    fqdn = container_app_details.configuration.ingress.fqdn
    logger.info(f"Container App deployed at: https://{fqdn}")

if __name__ == "__main__":
    create_managed_env()
    deploy_container_app()
