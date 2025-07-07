<script setup lang="ts">
  import type { PasteListItem } from '../types/paste';

  const props = defineProps<{paste: PasteListItem}>();
</script>

<template>
  <router-link :to="`/${paste.uuid}`">
    <h3>{{ paste.title }}</h3>
    <span>{{ new Date(paste.created_at).toLocaleString() }}</span>
  </router-link>
</template>

<style scoped></style>
