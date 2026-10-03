export type ServiceStatus = 'operational' | 'degraded' | 'outage'

export interface ApiStatus {
  status: ServiceStatus
  message: string
  inventoryBackend: string
  version: string
  recentErrors: number
}

export interface Product {
  id: string
  name: string
  category: string
  price: number
  rating: number
  stock: number
  packSize: number
  description: string
}

export interface ProductDetail extends Product {
  unitPrice: number
}

export interface ProductPage {
  items: Product[]
  total: number
  page: number
  pageSize: number
}

export interface ProductQuery {
  page: number
  pageSize: number
  sort: string
  order: 'asc' | 'desc'
  search?: string
  category?: string
}

export interface ApiError extends Error {
  status?: number
  correlationId: string
}
