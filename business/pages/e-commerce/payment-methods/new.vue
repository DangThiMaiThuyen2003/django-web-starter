<template>
  <div class="p-4 max-w-2xl">
      <h2 class="text-xl font-semibold mb-4">Create payment method</h2>
      <el-form :model="form" label-width="140px">
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
        <div class="flex gap-2">
          <el-button type="primary" @click="submit">Create</el-button>
          <NuxtLink to="/e-commerce/payment-methods" class="el-button">Back</NuxtLink>
        </div>
      </el-form>
    </div>
  <el-notification v-if="errorMessage" type="error" :title="'Error'" :message="errorMessage" />
  <el-notification v-if="successMessage" type="success" :title="'Success'" :message="successMessage" />
</template>

<script setup>
import service from '@/services/payment_methods'
definePageMeta({ layout: 'ecommerce' })
const router = useRouter()
const form = reactive({ name: '', method_type: 'offline', description: '', is_active: true })
const successMessage = ref('')
const errorMessage = ref('')

async function submit() {
  try {
    await service.create({ ...form })
    successMessage.value = 'Created successfully'
    router.push('/e-commerce/payment-methods')
  } catch (e) {
    errorMessage.value = e?.data?.detail || e?.message || 'Create failed'
  }
}
</script>

<style scoped></style>


