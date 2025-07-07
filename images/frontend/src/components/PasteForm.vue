<script setup lang="ts">
  import { ref } from 'vue';
  import type { PasteCreate } from '../types/paste';

  const props = defineProps<{
    onSubmit: (data: PasteCreate) => Promise<void>;
  }>();

  const form = ref<PasteCreate>(
    {
      title: '',
      text: '',
      expiration: '10_minutes',
      exposure: 'public',
    }
  );

  const handleSubmit = async () => {
    await props.onSubmit(form.value);
  };
</script>

<template>
  <form @submit.prevent="handleSubmit" class="paste-form">
    <div>
      <label for="title">Title</label>
      <input v-model="form.title" id="title" type="text" required />
    </div>

    <div>
      <label for="text">Content</label>
      <textarea v-model="form.text" id="text" rows="10" required></textarea>
    </div>

    <div>
      <label for="expiration">Expiration</label>
      <select v-model="form.expiration" id="expiration">
        <option value="10_minutes">10 minutes</option>
        <option value="1_hour">1 hour</option>
        <option value="1_day">1 day</option>
        <option value="1_week">1 week</option>
        <option value="1_month">1 month</option>
        <option value="1_year">1 year</option>
        <option value="never">Never</option>
        <option value="burn_after_read">Burn after read</option>
      </select>
    </div>

    <div>
      <label>Exposure</label>
      <div>
        <label>
          <input v-model="form.exposure" type="radio" value="public" />
          Public
        </label>
        <label>
          <input v-model="form.exposure" type="radio" value="unlisted" />
          Unlisted
        </label>
      </div>
    </div>

    <button type="submit">Create paste</button>
  </form>
</template>

<style scoped></style>
