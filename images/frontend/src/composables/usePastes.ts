import { ref } from 'vue';
import type { Paste, PasteCreate, PasteListItem } from '../types/paste';

const BASE_API_URL = import.meta.env.BACKEND_API_URL || 'http://127.0.0.1:8000';
const API_URL = BASE_API_URL + '/api/v1';

export const usePastes = () => {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const createPaste = async (pasteData: PasteCreate): Promise<Paste | null> => {
    try {
      loading.value = true;
      const response = await fetch(
        `${API_URL}/pastes`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pasteData),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to create paste');
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getPaste = async (uuid: string): Promise<Paste | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/pastes/${uuid}`);

      if (!response.ok) {
        throw new Error('Paste not found');
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getPastes = async (): Promise<PasteListItem[] | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/pastes`);

      if (!response.ok) {
        throw new Error('Failed to fetch pastes');
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      return null;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    createPaste,
    getPaste,
    getPastes,
  };
};
