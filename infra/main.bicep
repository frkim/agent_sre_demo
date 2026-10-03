targetScope = 'resourceGroup'

@description('Environment name used in all resource names.')
param environmentName string = 'demo'

@description('Azure region for all regional resources.')
param location string = resourceGroup().location

@description('API container image. Empty uses the demo placeholder image.')
param apiImage string = ''

@description('Web container image. Empty uses the demo placeholder image.')
param webImage string = ''

@description('Resource owner tag.')
param owner string

@description('Cost center tag.')
param costCenter string

@description('Principal object id that configures the SRE Agent data plane after deployment.')
param deployerPrincipalId string = ''

@allowed([
  'User'
  'Group'
  'ServicePrincipal'
  'ForeignGroup'
  'Device'
])
@description('Principal type for deployerPrincipalId.')
param deployerPrincipalType string = 'ServicePrincipal'

var workload = 'trek'
var placeholderImage = 'mcr.microsoft.com/k8se/quickstart:latest'
var effectiveApiImage = empty(apiImage) ? placeholderImage : apiImage
var effectiveWebImage = empty(webImage) ? placeholderImage : webImage
var tags = {
  env: environmentName
  workload: workload
  owner: owner
  costCenter: costCenter
  dataClassification: 'demo'
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring-${environmentName}'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
  }
}

module apps 'modules/container-apps.bicep' = {
  name: 'container-apps-${environmentName}'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    logAnalyticsCustomerId: monitoring.outputs.logAnalyticsCustomerId
    logAnalyticsSharedKey: monitoring.outputs.logAnalyticsSharedKey
    appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString
    apiImage: effectiveApiImage
    webImage: effectiveWebImage
  }
}

module sreAgent 'modules/sre-agent.bicep' = {
  name: 'sre-agent-${environmentName}'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    appInsightsAppId: monitoring.outputs.appInsightsAppId
    appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString
    appInsightsResourceId: monitoring.outputs.appInsightsResourceId
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsWorkspaceResourceId
    deployerPrincipalId: deployerPrincipalId
    deployerPrincipalType: deployerPrincipalType
  }
}

output webUrl string = 'https://${apps.outputs.webFqdn}'
output apiAppName string = apps.outputs.apiAppName
output webAppName string = apps.outputs.webAppName
output acrName string = apps.outputs.acrName
output acrLoginServer string = apps.outputs.acrLoginServer
output agentName string = sreAgent.outputs.sreAgentName
output agentEndpoint string = sreAgent.outputs.sreAgentEndpoint
output resourceGroupName string = resourceGroup().name
output logAnalyticsWorkspaceId string = monitoring.outputs.logAnalyticsWorkspaceResourceId
output appInsightsName string = monitoring.outputs.appInsightsName
