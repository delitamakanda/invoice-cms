<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const labels = {
  DRAFT: 'Draft',
  PDF_GENERATED: 'PDF generated',
  ACCEPTED: 'Accepted',
  REJECTED: 'Rejected',
  FAILED: 'Failed to generate PDF',
  SENT: 'Sent',
  READY_TO_SEND: 'Ready to send'
}
const message = computed(() => labels[props.status.toUpperCase()])

const classes = computed(() => [
    'inline-flex rounded-full px-2 py-1 text-xs font-medium text-gray-700',
  {
    'bg-gray-200': props.status === 'DRAFT',
    'bg-green-500': props.status === 'PDF_GENERATED',
    'bg-yellow-400': props.status === 'ACCEPTED',
    'bg-red-500': props.status === 'REJECTED',
    'bg-gray-400': props.status === 'FAILED',
    'bg-blue-500': props.status === 'SENT',
    'bg-orange-500': props.status === 'READY_TO_SEND'
  }
])
</script>

<template>
<span :class="classes">
  {{ message }}
</span>
</template>

<style scoped>

</style>