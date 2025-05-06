param storageAccountName string
param functionAppName string
param location string = 'East US 2'
param resourceGroupName string = resourceGroup().name

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  tags: {
    HU_BATCH: 'HU-DevOps-25'
    USER_NAME: 'rsingh95'
  }
}

// Blob service (required for the containers)
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2021-04-01' = {
  parent: storageAccount
  name: 'default'  // The default blob service name
}

// Container A
resource containerA 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-04-01' = {
  parent: blobService
  name: 'container-a'
}

// Container B
resource containerB 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-04-01' = {
  parent: blobService
  name: 'container-b'
}

// Function App Plan (Ensure this is a Function App Plan)
resource functionAppPlan 'Microsoft.Web/serverfarms@2021-03-01' = {
  name: 'functionAppPlan-${functionAppName}'
  location: location
  sku: {
    name: 'Y1'  // Consumption Plan (Y1 SKU)
    tier: 'Dynamic'
  }
  tags: {
    HU_BATCH: 'HU-DevOps-25'
    USER_NAME: 'rsingh95'
  }
}

// Function App (Ensure this is a Function App resource)
resource functionApp 'Microsoft.Web/sites@2021-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'  // Ensure this is a Function App and not a regular web app
  properties: {
    serverFarmId: functionAppPlan.id
  }
  tags: {
    HU_BATCH: 'HU-DevOps-25'
    USER_NAME: 'rsingh95'
  }
}
