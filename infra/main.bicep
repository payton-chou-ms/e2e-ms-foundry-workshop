// ========== main.bicep ========== //
targetScope = 'resourceGroup'
var abbrs = loadJsonContent('./abbreviations.json')
@minLength(3)
@maxLength(20)
@description('A unique prefix for all resources in this deployment. This should be 3-20 characters long:')
param environmentName string

@description('Optional. created by user name')
param createdBy string = contains(deployer(), 'userPrincipalName')
  ? split(deployer().userPrincipalName, '@')[0]
  : deployer().objectId

@minLength(1)
@description('GPT model deployment type:')
@allowed([
  'Standard'
  'GlobalStandard'
])
param deploymentType string = 'GlobalStandard'

@description('Name of the GPT model to deploy:')
param gptModelName string = 'gpt-4o-mini'

@description('Version of the GPT model to deploy:')
param gptModelVersion string = '2024-07-18'

@minValue(10)
@description('Capacity of the GPT deployment:')
// You can increase this, but capacity is limited per model/region, so you will get errors if you go over
// https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits
param gptDeploymentCapacity int = 150

@description('Optional. The tags to apply to all deployed Azure resources.')
param tags resourceInput<'Microsoft.Resources/resourceGroups@2025-04-01'>.tags = {}

@minLength(1)
@description('Name of the Text Embedding model to deploy:')
@allowed([
  'text-embedding-ada-002'
  'text-embedding-3-small'
  'text-embedding-3-large'
])
param embeddingModel string = 'text-embedding-ada-002'

@minValue(10)
@description('Capacity of the Embedding Model deployment')
param embeddingDeploymentCapacity int = 80

@description('Optional model deployments. Each entry can be enabled or disabled independently.')
param optionalModelDeployments array = []

@description('Whether to deploy a dedicated Azure OpenAI resource for image generation demos.')
param deployDedicatedImageOpenAI bool = true

@description('Azure region for the dedicated image-capable OpenAI resource.')
param imageOpenAILocation string = 'westus3'

@description('Image model deployment name for the dedicated image resource.')
param imageOpenAIDeploymentName string = 'gpt-image-1-5'

@description('Image model name for the dedicated image resource.')
param imageOpenAIModelName string = 'gpt-image-1.5'

@description('Image model version for the dedicated image resource.')
param imageOpenAIModelVersion string = '2025-12-16'

@description('Image model deployment SKU for the dedicated image resource.')
@allowed([
  'Standard'
  'GlobalStandard'
])
param imageOpenAIDeploymentSkuName string = 'GlobalStandard'

@minValue(1)
@description('Image model deployment capacity for the dedicated image resource.')
param imageOpenAIDeploymentCapacity int = 1

@description('Whether to deploy a Playwright Workspace for Browser Automation demos.')
param deployBrowserAutomation bool = true

@description('Azure region for the Playwright Workspace. Leave empty to use the resource group region when supported, otherwise eastus.')
param browserAutomationLocation string = ''

param AZURE_LOCATION string = ''
var solutionLocation = empty(AZURE_LOCATION) ? resourceGroup().location : AZURE_LOCATION

var uniqueId = toLower(uniqueString(subscription().id, environmentName, solutionLocation))
var browserAutomationSupportedLocations = [
  'eastus'
  'westus3'
  'westeurope'
  'eastasia'
]
var resolvedBrowserAutomationLocation = !empty(browserAutomationLocation)
  ? browserAutomationLocation
  : contains(browserAutomationSupportedLocations, toLower(solutionLocation)) ? solutionLocation : 'eastus'

@allowed([
  'australiaeast'
  'eastus'
  'eastus2'
  'francecentral'
  'japaneast'
  'swedencentral'
  'uksouth'
  'westus'
  'westus3'
])
@metadata({
  azd: {
    type: 'location'
    usageName: [
      'OpenAI.GlobalStandard.gpt-4o-mini,150'
      // 'OpenAI.GlobalStandard.text-embedding-ada-002,80'
    ]
  }
})
@description('Location for AI Foundry deployment. This is the location where the AI Foundry resources will be deployed.')
param aiDeploymentsLocation string

var solutionPrefix = 'da${padLeft(take(uniqueId, 12), 12, '0')}'

//Get the current deployer's information
var deployerInfo = deployer()
var deployingUserPrincipalId = deployerInfo.objectId

// ========== Resource Group Tag ========== //
resource resourceGroupTags 'Microsoft.Resources/tags@2021-04-01' = {
  name: 'default'
  properties: {
    tags: union(
      resourceGroup().tags ?? {},
      {
        TemplateName: 'IQs Workshop'
        CreatedBy: createdBy
      },
      tags
    )
  }
}
// AI Foundry Module (AI Services, Search, Storage, etc.)
module foundry './modules/foundry.bicep' = {
  params: {
    location: aiDeploymentsLocation
    tags: tags
    accountName: '${abbrs.ai.aiServices}${solutionPrefix}'
    projectName: '${abbrs.ai.aiFoundryProject}${solutionPrefix}'
    searchName: '${abbrs.ai.aiSearch}${solutionPrefix}'
    storageName: '${abbrs.storage.storageAccount}${solutionPrefix}'
    logAnalyticsName: '${abbrs.managementGovernance.logAnalyticsWorkspace}${solutionPrefix}'
    appInsightsName: '${abbrs.managementGovernance.applicationInsights}${solutionPrefix}'
    chatModel: gptModelName
    chatModelSkuName: deploymentType
    chatModelVersion: gptModelVersion
    chatModelCapacity: gptDeploymentCapacity
    embeddingModel: embeddingModel
    embeddingModelSkuName: 'Standard'
    embeddingModelCapacity: embeddingDeploymentCapacity
    optionalModelDeployments: optionalModelDeployments
    deployingUserPrincipalId: deployingUserPrincipalId
  }
}

module imageOpenAI './modules/image_openai.bicep' = if (deployDedicatedImageOpenAI) {
  params: {
    location: imageOpenAILocation
    tags: tags
    accountName: '${abbrs.ai.imageOpenAI}${take(uniqueId, 10)}'
    deploymentName: imageOpenAIDeploymentName
    modelName: imageOpenAIModelName
    modelVersion: imageOpenAIModelVersion
    deploymentSkuName: imageOpenAIDeploymentSkuName
    deploymentCapacity: imageOpenAIDeploymentCapacity
  }
}

module playwrightWorkspace './modules/playwright_workspace.bicep' = if (deployBrowserAutomation) {
  params: {
    location: resolvedBrowserAutomationLocation
    tags: tags
    workspaceName: '${abbrs.testing.playwrightWorkspace}${solutionPrefix}'
  }
}

// Outputs for azd (saved to .azure/<env>/.env)
output AZURE_LOCATION string = aiDeploymentsLocation
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_SUBSCRIPTION_ID string = subscription().subscriptionId
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output SOLUTION_PREFIX string = solutionPrefix

// AI Services
output AZURE_AI_SERVICES_NAME string = foundry.outputs.accountName
output AZURE_AI_SERVICES_RESOURCE_ID string = foundry.outputs.accountId
output AZURE_AI_PROJECT_NAME string = foundry.outputs.projectName
output AZURE_AI_PROJECT_RESOURCE_ID string = foundry.outputs.projectId
output AZURE_AI_PROJECT_PRINCIPAL_ID string = foundry.outputs.projectPrincipalId
output AZURE_AI_PROJECT_ENDPOINT string = foundry.outputs.projectEndpoint
output AZURE_AI_ENDPOINT string = foundry.outputs.aiEndpoint
output AZURE_OPENAI_ENDPOINT string = foundry.outputs.openAIEndpoint

// AI Search
output AZURE_AI_SEARCH_NAME string = foundry.outputs.searchName
output AZURE_AI_SEARCH_RESOURCE_ID string = foundry.outputs.searchId
output AZURE_AI_SEARCH_PRINCIPAL_ID string = foundry.outputs.searchPrincipalId
output AZURE_AI_SEARCH_ENDPOINT string = foundry.outputs.searchEndpoint
output AZURE_AI_PROJECT_SEARCH_CONNECTION_NAME string = foundry.outputs.searchConnectionName

// Storage
output AZURE_STORAGE_ACCOUNT_NAME string = foundry.outputs.storageName
output AZURE_STORAGE_ACCOUNT_RESOURCE_ID string = foundry.outputs.storageId
output AZURE_STORAGE_BLOB_ENDPOINT string = foundry.outputs.storageBlobEndpoint
output AZURE_AI_PROJECT_STORAGE_CONNECTION_NAME string = foundry.outputs.storageConnectionName

// Monitoring
output AZURE_APPINSIGHTS_NAME string = foundry.outputs.appInsightsName
output AZURE_APPINSIGHTS_RESOURCE_ID string = foundry.outputs.appInsightsId
output AZURE_APPINSIGHTS_CONNECTION_STRING string = foundry.outputs.appInsightsConnectionString
output AZURE_AI_PROJECT_APPINSIGHTS_CONNECTION_NAME string = foundry.outputs.appInsightsConnectionName
output AZURE_LOG_ANALYTICS_NAME string = foundry.outputs.logAnalyticsName
output AZURE_LOG_ANALYTICS_RESOURCE_ID string = foundry.outputs.logAnalyticsWorkspaceId

// Models
output AZURE_CHAT_MODEL string = gptModelName
output AZURE_EMBEDDING_MODEL string = embeddingModel
output AZURE_CHAT_DEPLOYMENT_NAME string = foundry.outputs.chatDeploymentName
output AZURE_EMBEDDING_DEPLOYMENT_NAME string = foundry.outputs.embeddingDeploymentName
output AZURE_CHAT_DEPLOYMENT_SKU string = foundry.outputs.chatDeploymentSkuName
output AZURE_EMBEDDING_DEPLOYMENT_SKU string = foundry.outputs.embeddingDeploymentSkuName
output AZURE_OPTIONAL_MODEL_DEPLOYMENTS array = foundry.outputs.optionalModelDeployments
output AZURE_ENABLED_OPTIONAL_MODEL_DEPLOYMENT_NAMES array = foundry.outputs.enabledOptionalModelDeploymentNames
output AZURE_SKIPPED_OPTIONAL_MODEL_DEPLOYMENT_NAMES array = foundry.outputs.skippedOptionalModelDeploymentNames
output AZURE_DEPLOYED_MODEL_SUMMARIES array = foundry.outputs.deployedModelSummaries
output AZURE_IMAGE_OPENAI_NAME string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.accountName : ''
output AZURE_IMAGE_OPENAI_RESOURCE_ID string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.accountId : ''
output AZURE_IMAGE_OPENAI_ENDPOINT string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.endpoint : ''
output AZURE_IMAGE_OPENAI_LOCATION string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.location : ''
output AZURE_IMAGE_MODEL_DEPLOYMENT string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.deploymentName : ''
output AZURE_IMAGE_MODEL_NAME string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.modelName : ''
output AZURE_IMAGE_MODEL_VERSION string = deployDedicatedImageOpenAI ? imageOpenAI!.outputs.modelVersion : ''
output AZURE_PLAYWRIGHT_WORKSPACE_NAME string = deployBrowserAutomation
  ? playwrightWorkspace!.outputs.workspaceName
  : ''
output AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID string = deployBrowserAutomation
  ? playwrightWorkspace!.outputs.workspaceResourceId
  : ''
output AZURE_PLAYWRIGHT_WORKSPACE_ID string = deployBrowserAutomation ? playwrightWorkspace!.outputs.workspaceId : ''
output AZURE_PLAYWRIGHT_LOCATION string = deployBrowserAutomation ? playwrightWorkspace!.outputs.location : ''
output AZURE_PLAYWRIGHT_DATAPLANE_URI string = deployBrowserAutomation ? playwrightWorkspace!.outputs.dataplaneUri : ''
output AZURE_PLAYWRIGHT_BROWSER_ENDPOINT string = deployBrowserAutomation
  ? playwrightWorkspace!.outputs.browserEndpoint
  : ''
output AZURE_PLAYWRIGHT_AUTH_MODE string = deployBrowserAutomation
  ? 'Playwright Service Access Token (manual token generation still required)'
  : ''
