import os
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.web import WebSiteManagementClient
from dotenv import load_dotenv

load_dotenv()

subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("RESOURCE_GROUP")
tag_key = os.getenv("TAG_KEY")
tag_value = os.getenv("TAG_VALUE")

print(f"Subscription ID: {subscription_id}")
print(f"Resource Group: {resource_group}")
print(f"Tag Key: {tag_key}")
print(f"Tag Value: {tag_value}")

credential = AzureCliCredential()
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
web_client = WebSiteManagementClient(credential, subscription_id)

def get_api_version(resource_type):
    """Retrieve the latest API version for a given resource type."""
    provider, type_name = resource_type.split('/', 1)
    rp = resource_client.providers.get(provider)
    for rt in rp.resource_types:
        if rt.resource_type.lower() == type_name.lower():
            return rt.api_versions[0]  # Pick the first (latest) API version
    return None

def delete_resource(resource):
    """Delete a resource based on its type."""
    try:
        if "storageAccounts" in resource.type:
            storage_client.storage_accounts.delete(resource_group, resource.name)
        elif "sites" in resource.type:
            web_client.web_apps.delete(resource_group, resource.name)
        elif "serverfarms" in resource.type:
            web_client.app_service_plans.delete(resource_group, resource.name)
        else:
            api_version = get_api_version(resource.type)
            if not api_version:
                print(f"API version not found for: {resource.type}")
                return
            resource_client.resources.begin_delete_by_id(resource.id, api_version).wait()
        print(f"Deleted: {resource.name}")
    except Exception as e:
        print(f"Failed to delete {resource.name}: {e}")

def main():
    """Main function to list and delete resources based on tags."""
    print("Fetching resources...")
    resources = resource_client.resources.list_by_resource_group(resource_group)

    for resource in resources:
        if resource.tags and resource.tags.get(tag_key) == tag_value:
            print(f"Deleting: {resource.name} ({resource.type})")
            delete_resource(resource)

if __name__ == "__main__":
    main()