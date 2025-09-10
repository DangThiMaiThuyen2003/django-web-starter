<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <div class="w-full max-w-3xl bg-white rounded shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold">Create payment method</h2>
        <NuxtLink to="/e-commerce/payment-methods" class="text-primary">Back</NuxtLink>
      </div>
      <el-form :model="form" label-width="160px" @submit.prevent="submit">
        <el-form-item label="Name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Type">
          <el-select v-model="form.method_type" placeholder="Select type">
            <el-option label="offline" value="offline" />
            <el-option label="online" value="online" />
          </el-select>
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="form.description" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="Active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
        <el-form-item>
          <div class="flex gap-2">
            <el-button type="primary" native-type="submit" :loading="loading" :disabled="!form.name || !form.method_type">Create</el-button>
            <NuxtLink to="/e-commerce/payment-methods" class="el-button">Cancel</NuxtLink>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
  <el-notification v-if="errorMessage" type="error" :title="'Error'" :message="errorMessage" />
  <el-notification v-if="successMessage" type="success" :title="'Success'" :message="successMessage" />
</template>

<script setup>
import service from '@/services/payment_methods'
definePageMeta({ layout: 'ecommerce' })
const router = useRouter()
const form = reactive({ name: '', method_type: 'offline', description: '', is_active: true })
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

async function submit() {
  try {
    loading.value = true
    await service.create({ ...form })
    successMessage.value = 'Created successfully'
    router.push('/e-commerce/payment-methods')
  } catch (e) {
    errorMessage.value = e?.data?.detail || e?.message || 'Create failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>


