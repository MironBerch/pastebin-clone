<script setup lang="ts">
  import { onMounted, ref } from 'vue';
  import { useRoute } from 'vue-router';

  import { usePastes } from '../composables/usePastes';
  import PasteView from '../components/PasteView.vue';

  const route = useRoute();
  const { getPaste, loading, error } = usePastes();
  const paste = ref<any>(null);

  onMounted(
    async () => {
      paste.value = await getPaste(route.params.uuid as string);
    }
  );
</script>

<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
    <PasteView v-if="paste" :paste="paste" />
  </div>
</template>

<style scoped></style>
