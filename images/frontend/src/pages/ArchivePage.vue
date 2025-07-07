<script setup lang="ts">
  import { onMounted, ref } from 'vue';

  import { usePastes } from '../composables/usePastes';
  import PasteItem from '../components/PasteItem.vue';

  const { getPastes, loading, error } = usePastes();
  const pastes = ref<any[]>([]);

  onMounted(
    async () => {
      const data = await getPastes();
      if (data) {
        pastes.value = data;
      }
    }
  );
</script>

<template>
  <div>
    <h1>Paste Archive</h1>
    <div v-if="loading">Loading pastes...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="pastes.length === 0 && !loading">No pastes found</div>
    <div>
      <PasteItem v-for="paste in pastes" :key="paste.uuid" :paste="paste" />
    </div>
  </div>
</template>

<style scoped></style>
