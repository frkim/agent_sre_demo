<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useTheme } from 'vuetify'

import { fetchCategories, fetchProductDetail, fetchProducts, fetchStatus } from './services/api'
import type { ApiError, ApiStatus, Product, ProductDetail, ProductQuery } from './types'
import { mapStatusToBanner } from './utils/status'

interface TableOptions {
  page: number
  itemsPerPage: number
  sortBy: { key: string; order?: 'asc' | 'desc' }[]
}

const theme = useTheme()
const status = ref<ApiStatus | null>(null)
const lastChecked = ref<Date | null>(null)
const products = ref<Product[]>([])
const productTotal = ref(0)
const loadingProducts = ref(false)
const categories = ref<string[]>([])
const selectedCategory = ref<string | null>(null)
const searchText = ref('')
const debouncedSearch = ref('')
const page = ref(1)
const itemsPerPage = ref(10)
const sortBy = ref<TableOptions['sortBy']>([{ key: 'name', order: 'asc' }])
const detailOpen = ref(false)
const detailLoading = ref(false)
const selectedProduct = ref<ProductDetail | null>(null)
const detailError = ref<{ message: string; correlationId: string } | null>(null)
let statusTimer: number | undefined
let debounceTimer: ReturnType<typeof setTimeout> | undefined

const headers = [
  { title: 'Product', key: 'name', sortable: true },
  { title: 'Category', key: 'category', sortable: true },
  { title: 'Price', key: 'price', sortable: true },
  { title: 'Rating', key: 'rating', sortable: true },
  { title: 'Stock', key: 'stock', sortable: false },
]

const banner = computed(() => mapStatusToBanner(status.value?.status ?? 'operational'))
const footerText = computed(() => {
  const version = status.value?.version ?? 'unknown'
  const backend = status.value?.inventoryBackend ?? 'unknown'
  return `API ${version} · inventory backend: ${backend}`
})
const themeIcon = computed(() =>
  theme.global.current.value.dark ? 'mdi-weather-night' : 'mdi-white-balance-sunny'
)
const themeLabel = computed(() =>
  theme.global.current.value.dark ? 'Use light theme' : 'Use dark theme'
)

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

function formatChecked(value: Date | null): string {
  return value
    ? value.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : 'never'
}

function applyInitialTheme(): void {
  const saved = localStorage.getItem('contoso-trek-theme')
  if (saved === 'light' || saved === 'dark') {
    theme.global.name.value = saved
    return
  }
  theme.global.name.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light'
}

function toggleTheme(): void {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  localStorage.setItem('contoso-trek-theme', theme.global.name.value)
}

async function refreshStatus(): Promise<void> {
  try {
    status.value = await fetchStatus()
    lastChecked.value = new Date()
  } catch {
    status.value = {
      status: 'outage',
      message: 'Status endpoint is unavailable.',
      inventoryBackend: 'unknown',
      version: 'unknown',
      recentErrors: 0,
    }
    lastChecked.value = new Date()
  }
}

async function loadCategories(): Promise<void> {
  try {
    categories.value = await fetchCategories()
  } catch {
    categories.value = []
  }
}

function currentProductQuery(): ProductQuery {
  const sort = sortBy.value[0]
  return {
    page: page.value,
    pageSize: itemsPerPage.value,
    sort: sort?.key ?? 'name',
    order: sort?.order ?? 'asc',
    search: debouncedSearch.value || undefined,
    category: selectedCategory.value || undefined,
  }
}

async function loadProducts(): Promise<void> {
  loadingProducts.value = true
  try {
    const result = await fetchProducts(currentProductQuery())
    products.value = result.items
    productTotal.value = result.total
  } finally {
    loadingProducts.value = false
  }
}

function updateTable(options: TableOptions): void {
  page.value = options.page
  itemsPerPage.value = options.itemsPerPage
  sortBy.value = options.sortBy.length ? options.sortBy : [{ key: 'name', order: 'asc' }]
  void loadProducts()
}

async function openDetail(_: Event, row: { item: Product }): Promise<void> {
  detailOpen.value = true
  detailLoading.value = true
  selectedProduct.value = null
  detailError.value = null
  try {
    selectedProduct.value = await fetchProductDetail(row.item.id)
  } catch (error) {
    const apiError = error as ApiError
    detailError.value = {
      message: 'We could not load this product right now. Please try another item or contact support.',
      correlationId: apiError.correlationId,
    }
  } finally {
    detailLoading.value = false
  }
}

watch(searchText, (value) => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = setTimeout(() => {
    debouncedSearch.value = value.trim()
    page.value = 1
    void loadProducts()
  }, 300)
})

watch(selectedCategory, () => {
  page.value = 1
  void loadProducts()
})

onMounted(() => {
  applyInitialTheme()
  void refreshStatus()
  void loadCategories()
  void loadProducts()
  statusTimer = window.setInterval(() => void refreshStatus(), 5000)
})

onUnmounted(() => {
  if (statusTimer) {
    window.clearInterval(statusTimer)
  }
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="comfortable" elevation="2">
      <v-app-bar-title class="font-weight-bold">Contoso Trek</v-app-bar-title>
      <v-spacer />
      <v-btn :aria-label="themeLabel" :title="themeLabel" :icon="themeIcon" variant="text" @click="toggleTheme" />
    </v-app-bar>

    <v-main>
      <v-container class="py-8" max-width="1180">
        <v-alert
          class="mb-6 status-banner"
          :color="banner.color"
          :icon="banner.icon"
          border="start"
          variant="tonal"
          aria-live="polite"
          role="status"
        >
          <div class="d-flex flex-column flex-sm-row ga-2 align-sm-center justify-space-between">
            <div>
              <div class="text-h6 font-weight-bold">{{ banner.label }}</div>
              <div>{{ status?.message ?? 'Checking system status…' }}</div>
            </div>
            <div class="text-caption">Last checked: {{ formatChecked(lastChecked) }}</div>
          </div>
        </v-alert>

        <v-card elevation="3" rounded="xl">
          <v-card-title class="d-flex flex-column flex-md-row ga-4 align-md-center justify-space-between pa-6">
            <div>
              <div class="text-h5 font-weight-bold">Outdoor gear catalog</div>
              <div class="text-body-2 text-medium-emphasis">
                Browse reliable equipment for the next trail, crag, or lake day.
              </div>
            </div>
            <div class="d-flex flex-column flex-sm-row ga-3 filters">
              <v-select
                v-model="selectedCategory"
                :items="categories"
                label="Category"
                clearable
                density="comfortable"
                hide-details
                min-width="190"
              />
              <v-text-field
                v-model="searchText"
                label="Search products"
                prepend-inner-icon="mdi-magnify"
                density="comfortable"
                hide-details
                clearable
                min-width="240"
              />
            </div>
          </v-card-title>

          <v-data-table-server
            v-model:page="page"
            v-model:items-per-page="itemsPerPage"
            v-model:sort-by="sortBy"
            :headers="headers"
            :items="products"
            :items-length="productTotal"
            :loading="loadingProducts"
            item-value="id"
            hover
            class="catalog-table"
            @update:options="updateTable"
            @click:row="openDetail"
          >
            <template #item.name="{ item }">
              <div class="font-weight-medium">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.description }}</div>
            </template>
            <template #item.price="{ item }">{{ formatCurrency(item.price) }}</template>
            <template #item.rating="{ item }">
              <v-chip color="secondary" size="small" prepend-icon="mdi-star">
                {{ item.rating.toFixed(1) }}
              </v-chip>
            </template>
            <template #item.stock="{ item }">
              <span :class="item.stock < 15 ? 'text-warning font-weight-bold' : ''">
                {{ item.stock }}
              </span>
            </template>
          </v-data-table-server>
        </v-card>
      </v-container>
    </v-main>

    <v-footer class="justify-center text-caption" border>{{ footerText }}</v-footer>

    <v-dialog v-model="detailOpen" max-width="620">
      <v-card rounded="xl">
        <v-card-title class="d-flex align-center justify-space-between">
          <span>Product detail</span>
          <v-btn icon="mdi-close" aria-label="Close product detail" variant="text" @click="detailOpen = false" />
        </v-card-title>
        <v-divider />
        <v-card-text>
          <v-progress-linear v-if="detailLoading" indeterminate color="primary" />
          <v-alert v-else-if="detailError" type="error" variant="tonal" prominent>
            <div class="font-weight-bold">{{ detailError.message }}</div>
            <div class="text-caption mt-2">Correlation ID: {{ detailError.correlationId }}</div>
          </v-alert>
          <div v-else-if="selectedProduct" class="detail-grid">
            <div>
              <div class="text-h5 font-weight-bold">{{ selectedProduct.name }}</div>
              <div class="text-medium-emphasis mb-4">{{ selectedProduct.category }}</div>
              <p>{{ selectedProduct.description }}</p>
            </div>
            <v-list density="compact" lines="one">
              <v-list-item title="Price" :subtitle="formatCurrency(selectedProduct.price)" />
              <v-list-item title="Unit price" :subtitle="formatCurrency(selectedProduct.unitPrice)" />
              <v-list-item title="Pack size" :subtitle="String(selectedProduct.packSize)" />
              <v-list-item title="Rating" :subtitle="`${selectedProduct.rating.toFixed(1)} / 5`" />
              <v-list-item title="Stock" :subtitle="`${selectedProduct.stock} available`" />
            </v-list>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<style scoped>
.status-banner {
  letter-spacing: 0.01em;
}

.filters {
  width: min(100%, 520px);
}

.catalog-table :deep(tbody tr) {
  cursor: pointer;
}

.detail-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) 220px;
}

@media (max-width: 700px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
