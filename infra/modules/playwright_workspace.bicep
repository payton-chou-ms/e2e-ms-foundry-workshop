@description('Azure region for the Playwright Workspace')
param location string

@description('Resource tags')
param tags object = {}

@description('Playwright Workspace resource name')
param workspaceName string

resource playwrightWorkspace 'Microsoft.LoadTestService/playwrightWorkspaces@2025-09-01' = {
  name: workspaceName
  location: location
  tags: tags
  properties: {
    localAuth: 'Enabled'
    regionalAffinity: 'Enabled'
  }
}

var dataplaneUri = playwrightWorkspace.properties.?dataplaneUri ?? ''
var browserEndpoint = empty(dataplaneUri) ? '' : '${replace(dataplaneUri, 'https://', 'wss://')}/browsers'

output workspaceName string = playwrightWorkspace.name
output workspaceId string = playwrightWorkspace.properties.?workspaceId ?? ''
output workspaceResourceId string = playwrightWorkspace.id
output dataplaneUri string = dataplaneUri
output browserEndpoint string = browserEndpoint
output location string = playwrightWorkspace.location
output localAuth string = playwrightWorkspace.properties.?localAuth ?? 'Enabled'
