@description('Azure region for the dedicated image-capable OpenAI resource')
param location string

@description('Resource tags')
param tags object = {}

@description('Dedicated Azure OpenAI account name for image generation')
param accountName string

@description('Image deployment name')
param deploymentName string

@description('Azure OpenAI image model name')
param modelName string

@description('Azure OpenAI image model version')
param modelVersion string

@description('Deployment SKU name for the image model')
@allowed([
  'Standard'
  'GlobalStandard'
])
param deploymentSkuName string = 'GlobalStandard'

@description('Deployment capacity for the image model')
param deploymentCapacity int = 1

@description('Whether to disable local auth and rely on AAD for the image endpoint')
param disableLocalAuth bool = true

resource imageAccount 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: accountName
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: accountName
    disableLocalAuth: disableLocalAuth
    publicNetworkAccess: 'Enabled'
  }
}

resource imageDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview' = {
  parent: imageAccount
  name: deploymentName
  sku: {
    name: deploymentSkuName
    capacity: deploymentCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
  }
}

output accountName string = imageAccount.name
output accountId string = imageAccount.id
output endpoint string = imageAccount.properties.endpoint
output deploymentName string = imageDeployment.name
output location string = imageAccount.location
output modelName string = modelName
output modelVersion string = modelVersion
output disableLocalAuth bool = imageAccount.properties.disableLocalAuth
