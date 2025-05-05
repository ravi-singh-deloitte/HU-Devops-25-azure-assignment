param (
    [string]$username = "rsingh95",
    [string]$subscriptionId,
    [string]$resourceGroup,
    [string]$storageAccount,
    [string]$container
)

$fileName = "${username}_sub_Vnet.csv"

az account set --subscription $subscriptionId

# Get VNets and subnets

$vnetData = az network vnet list --query "[].{VNet:name, Subnets:join(',', subnets[].name)}" -o tsv
$vnetData | Out-File -FilePath $fileName

# Upload CSV to blob container
# Upload CSV with key authentication
az storage blob upload `
  --account-name $storageAccount `
  --container-name $container `
  --name $fileName `
  --file $fileName `
  --auth-mode key


  
