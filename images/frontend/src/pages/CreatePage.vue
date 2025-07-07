<script setup lang="ts">
  import { useRouter } from 'vue-router';
  import { usePastes } from '../composables/usePastes';

  import PasteForm from '../components/PasteForm.vue';

  const router = useRouter();
  const { createPaste, loading, error } = usePastes();

  const handleSubmit = async (data: PasteCreate) => {
    const paste = await createPaste(data);
    if (paste) {
      router.push(`/${paste.uuid}`);
    }
  };
</script>

<template>
  <div>
    <h1>Create New Paste</h1>
    <PasteForm :onSubmit="handleSubmit" />
    <div v-if="loading">Creating paste...</div>
    <div v-if="error">{{ error }}</div>
  </div>
</template>

<style scoped></style>
