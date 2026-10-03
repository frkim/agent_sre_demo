import { describe, expect, it } from 'vitest'

import { mapStatusToBanner } from './status'

describe('mapStatusToBanner', () => {
  it('maps operational status to a green banner', () => {
    expect(mapStatusToBanner('operational')).toEqual({
      color: 'success',
      icon: 'mdi-check-circle',
      label: 'ALL SYSTEMS OPERATIONAL',
    })
  })

  it('maps degraded and outage statuses to warning states', () => {
    expect(mapStatusToBanner('degraded').label).toBe('DEGRADED')
    expect(mapStatusToBanner('degraded').color).toBe('warning')
    expect(mapStatusToBanner('outage').label).toBe('OUTAGE')
    expect(mapStatusToBanner('outage').color).toBe('error')
  })
})
