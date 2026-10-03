param environmentName string
param location string
param tags object
param appInsightsAppId string
@secure()
param appInsightsConnectionString string
param appInsightsResourceId string
param logAnalyticsWorkspaceId string
param deployerPrincipalId string = ''
param deployerPrincipalType string = 'ServicePrincipal'

var sreAgentName = 'sre-trek-${environmentName}'
var sreAgentIdentityName = 'id-sre-trek-${environmentName}'
var actionGroupName = 'ag-sre-trek-${environmentName}'
var appExceptionAlertName = 'alert-trek-app-exception-${environmentName}'
var availabilityAlertName = 'alert-trek-availability-${environmentName}'

var readerRoleId = 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
var monitoringReaderRoleId = '43d0d8ad-25c7-4714-9337-8ba259a9fe05'
var logAnalyticsReaderRoleId = '73c42c96-874c-492b-b04d-ab87d138a893'
var containerAppsContributorRoleId = '358470bc-b998-42bd-ab17-a7e34c199c0f'
var sreAgentAdministratorRoleId = 'e79298df-d852-4c6d-84f9-5d13249d1e55'

resource sreAgentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: sreAgentIdentityName
  location: location
  tags: tags
}

resource readerAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, sreAgentIdentity.id, readerRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', readerRoleId)
    principalId: sreAgentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource monitoringReaderAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, sreAgentIdentity.id, monitoringReaderRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', monitoringReaderRoleId)
    principalId: sreAgentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource logAnalyticsReaderAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, sreAgentIdentity.id, logAnalyticsReaderRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', logAnalyticsReaderRoleId)
    principalId: sreAgentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource containerAppsContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, sreAgentIdentity.id, containerAppsContributorRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', containerAppsContributorRoleId)
    principalId: sreAgentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource sreAgentActionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: actionGroupName
  location: 'global'
  tags: tags
  properties: {
    groupShortName: 'sretrek'
    enabled: true
  }
}

resource sreAgent 'Microsoft.App/agents@2026-01-01' = {
  name: sreAgentName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned, UserAssigned'
    userAssignedIdentities: {
      '${sreAgentIdentity.id}': {}
    }
  }
  properties: {
    upgradeChannel: 'Stable'
    knowledgeGraphConfiguration: {
      identity: sreAgentIdentity.id
      managedResources: [
        resourceGroup().id
      ]
    }
    logConfiguration: {
      applicationInsightsConfiguration: {
        appId: appInsightsAppId
        connectionString: appInsightsConnectionString
      }
    }
    actionConfiguration: {
      identity: sreAgentIdentity.id
      mode: 'Autonomous'
      accessLevel: 'High'
    }
    incidentManagementConfiguration: {
      type: 'AzMonitor'
      connectionName: 'azmonitor'
    }
    defaultModel: {
      provider: 'Anthropic'
      name: 'Automatic'
    }
    #disable-next-line BCP037 // Preview SRE Agent fields are accepted by ARM before the Bicep type is updated.
    experimentalSettings: {
      EnableWorkspaceTools: true
      EnableHttpTriggers: true
      EnableV2AgentLoop: true
    }
  }

  resource applicationInsightsConnector 'connectors' = {
    name: 'app-insights'
    properties: {
      dataConnectorType: 'AppInsights'
      #disable-next-line use-secure-value-for-secure-inputs // The preview connector API expects the App Insights connection string in dataSource.
      dataSource: appInsightsConnectionString
      extendedProperties: {
        armResourceId: appInsightsResourceId
        resource: {
          name: last(split(appInsightsResourceId, '/'))
        }
        appId: appInsightsAppId
      }
      identity: 'system'
    }
  }
}

resource deployerSreAdminAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(deployerPrincipalId)) {
  name: guid(sreAgent.id, deployerPrincipalId, sreAgentAdministratorRoleId)
  scope: sreAgent
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', sreAgentAdministratorRoleId)
    principalId: deployerPrincipalId
    principalType: deployerPrincipalType
  }
}

resource appExceptionAlert 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: appExceptionAlertName
  location: location
  tags: tags
  properties: {
    displayName: appExceptionAlertName
    description: 'Contoso Trek product detail pages are returning HTTP 500 responses and unhandled exceptions are being recorded by the API.'
    severity: 2
    enabled: true
    scopes: [
      logAnalyticsWorkspaceId
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT5M'
    skipQueryValidation: true
    autoMitigate: true
    criteria: {
      allOf: [
        {
          query: 'AppExceptions | where AppRoleName startswith "ca-trek-api"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: {
            numberOfEvaluationPeriods: 1
            minFailingPeriodsToAlert: 1
          }
        }
      ]
    }
    actions: {
      actionGroups: [
        sreAgentActionGroup.id
      ]
    }
  }
}

resource availabilityAlert 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: availabilityAlertName
  location: location
  tags: tags
  properties: {
    displayName: availabilityAlertName
    description: 'Contoso Trek catalog requests are returning HTTP 503 responses from the API.'
    severity: 1
    enabled: true
    scopes: [
      logAnalyticsWorkspaceId
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT5M'
    skipQueryValidation: true
    autoMitigate: true
    criteria: {
      allOf: [
        {
          query: 'AppRequests | where AppRoleName startswith "ca-trek-api" | where ResultCode == "503"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 3
          failingPeriods: {
            numberOfEvaluationPeriods: 1
            minFailingPeriodsToAlert: 1
          }
        }
      ]
    }
    actions: {
      actionGroups: [
        sreAgentActionGroup.id
      ]
    }
  }
}

output sreAgentName string = sreAgent.name
output sreAgentIdentityId string = sreAgentIdentity.id
output sreAgentIdentityPrincipalId string = sreAgentIdentity.properties.principalId
#disable-next-line use-resource-symbol-reference // The preview agentEndpoint property is not exposed on the Bicep resource type yet.
output sreAgentEndpoint string = reference(sreAgent.id, '2026-01-01').properties.agentEndpoint
output sreAgentAdministratorRoleName string = 'SRE Agent Administrator'
output sreAgentAdministratorRoleId string = sreAgentAdministratorRoleId
