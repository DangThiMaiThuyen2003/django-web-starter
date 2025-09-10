<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <div class="w-full max-w-screen-xl px-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Payment methods</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-3 mb-4">
        <el-input v-model="filters.keyword" placeholder="Search by name" clearable />
        <el-select v-model="filters.method_type" clearable placeholder="Type">
          <el-option label="offline" value="offline" />
          <el-option label="online" value="online" />
        </el-select>
        <el-select v-model="filters.is_active" clearable placeholder="Status">
          <el-option label="Active" :value="true" />
          <el-option label="Inactive" :value="false" />
        </el-select>
        <div class="flex gap-2">
          <el-button type="primary" @click="load()">Filter</el-button>
          <el-button @click="resetFilters">Reset</el-button>
        </div>
      </div>

      <el-table :data="items" border style="width: 100%" @selection-change="onSelectionChange">
        <el-table-column type="selection" width="45" />
        <el-table-column prop="name" label="Name" min-width="220" />
        <el-table-column prop="method_type" label="Type" width="140" />
        <el-table-column prop="description" label="Description" min-width="260" />
        <el-table-column prop="updated_at" label="Updated at" min-width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Status" width="140">
          <template #default="{ row }">
            <div class="flex items-center gap-2">
              <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? 'Active' : 'Inactive' }}</el-tag>
              <el-switch :model-value="row.is_active" @change="val => toggleOne(row, val)" />
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-3 flex items-center gap-2">
        <el-button :disabled="selectedIds.length===0" @click="bulkToggle(true)">Set Active</el-button>
        <el-button :disabled="selectedIds.length===0" @click="bulkToggle(false)">Set Inactive</el-button>
      </div>

      <div class="mt-4 flex justify-end">
        <NuxtLink
          to="/e-commerce/payment-methods/new"
          class="inline-flex items-center bg-red-700 text-white px-4 py-2 rounded shadow hover:opacity-90"
        >
          <span class="text-lg mr-2">+</span>
          <span>New</span>
        </NuxtLink>
      </div>
    </div>
  </div>
  <el-notification v-if="errorMessage" type="error" :title="'Error'" :message="errorMessage" />
  <el-notification v-if="successMessage" type="success" :title="'Success'" :message="successMessage" />
</template>

<script setup>
import service from '@/services/payment_methods'
import PaginationTable from '@/components/PaginationTable.vue'
import { formatDateTime } from '~/utils/time'
import { useOauthStore } from '@/stores/oauth'
definePageMeta({ layout: 'ecommerce' })
const successMessage = ref('')
const errorMessage = ref('')
const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:payment-methods:edit"]))

// data
const items = ref([])
const selectedIds = ref([])
const filters = reactive({ keyword: '', method_type: undefined, is_active: undefined })

function resetFilters() {
  filters.keyword = ''
  filters.method_type = undefined
  filters.is_active = undefined
  load()
}

function onSelectionChange(rows) {
  selectedIds.value = rows.map(r => r.id)
}

async function load() {
  try {
    const params = {}
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.method_type) params.method_type = filters.method_type
    if (typeof filters.is_active === 'boolean') params.is_active = filters.is_active
    const res = await service.gets(params)
    items.value = res
  } catch (e) {
    errorMessage.value = e?.data?.detail || e?.message || 'Load failed'
  }
}

async function bulkToggle(active) {
  try {
    await service.bulkToggle(selectedIds.value, active)
    successMessage.value = 'Updated successfully'
    await load()
  } catch (e) {
    errorMessage.value = e?.data?.detail || e?.message || 'Update failed'
  }
}

async function toggleOne(row, val) {
  try {
    await service.update({ id: row.id, is_active: val })
    await load()
  } catch (e) {
    errorMessage.value = e?.data?.detail || e?.message || 'Update failed'
  }
}

onMounted(load)
</script>

<style scoped></style>


