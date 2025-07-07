<script setup lang="ts">
  import type { Paste } from '../types/paste';

  const props = defineProps<{paste: Paste;}>();
</script>

<template>
  <div>
    <h1>{{ paste.title }}</h1>
    <div>
      <span>Created: {{ new Date(paste.created_at).toLocaleString() }}</span>
      <span v-if="paste.expiration">Expires: {{ paste.expiration }}</span>
      <span>Visibility: {{ paste.exposure }}</span>
    </div>
    <pre>{{ paste.text }}</pre>
  </div>
</template>

<style scoped></style>
