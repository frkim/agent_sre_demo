import type { ApiError, ApiStatus, ProductDetail, ProductPage, ProductQuery } from '../types'

function makeCorrelationId(): string {
  return globalThis.crypto?.randomUUID?.() ?? `corr-${Date.now()}`
}

async function requestJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  const correlationId = makeCorrelationId()
  const response = await fetch(path, {
    ...init,
    headers: {
      Accept: 'application/json',
      'x-correlation-id': correlationId,
      ...init.headers,
    },
  })

  const contentType = response.headers.get('content-type') ?? ''
  const body = contentType.includes('application/json') ? await response.json() : undefined
  if (!response.ok) {
    const error = new Error(`Request failed with HTTP ${response.status}`) as ApiError
    error.status = response.status
    error.correlationId = body?.correlationId ?? response.headers.get('x-correlation-id') ?? correlationId
    throw error
  }
  return body as T
}

export function fetchStatus(): Promise<ApiStatus> {
  return requestJson<ApiStatus>('/api/v1/status')
}

export function fetchCategories(): Promise<string[]> {
  return requestJson<string[]>('/api/v1/categories')
}

export function fetchProducts(query: ProductQuery): Promise<ProductPage> {
  const params = new URLSearchParams({
    page: String(query.page),
    pageSize: String(query.pageSize),
    sort: query.sort,
    order: query.order,
  })
  if (query.search) {
    params.set('search', query.search)
  }
  if (query.category) {
    params.set('category', query.category)
  }
  return requestJson<ProductPage>(`/api/v1/products?${params}`)
}

export function fetchProductDetail(productId: string): Promise<ProductDetail> {
  return requestJson<ProductDetail>(`/api/v1/products/${encodeURIComponent(productId)}`)
}
