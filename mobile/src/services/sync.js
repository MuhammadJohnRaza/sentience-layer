import { apiClient } from './api';

export const syncService = {
  /**
   * Pushes an array of offline actions to the Sentience backend
   * @param {Array} queue - Array of action objects
   */
  async pushOfflineQueue(queue) {
    if (!queue || queue.length === 0) return true;
    
    console.log(`[SyncService] Pushing ${queue.length} items to kernel...`);
    try {
      const response = await apiClient.post('/sync/batch', { actions: queue });
      return response.success;
    } catch (error) {
      console.error('[SyncService] Batch sync failed', error);
      throw error;
    }
  },

  /**
   * Fetches the latest global state from the kernel to reconcile local storage
   */
  async pullLatestState() {
    try {
      return await apiClient.get('/sync/state');
    } catch (error) {
      console.error('[SyncService] State pull failed', error);
      throw error;
    }
  }
};
