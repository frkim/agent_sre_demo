import type { ServiceStatus } from '../types'

export interface BannerPresentation {
  color: 'success' | 'warning' | 'error'
  icon: string
  label: string
}

export function mapStatusToBanner(status: ServiceStatus): BannerPresentation {
  switch (status) {
    case 'operational':
      return { color: 'success', icon: 'mdi-check-circle', label: 'ALL SYSTEMS OPERATIONAL' }
    case 'degraded':
      return { color: 'warning', icon: 'mdi-alert', label: 'DEGRADED' }
    case 'outage':
      return { color: 'error', icon: 'mdi-alert-octagon', label: 'OUTAGE' }
  }
}
