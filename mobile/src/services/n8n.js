import { apiClient } from './api';

export const n8nService = {
  /**
   * Triggers a specific n8n workflow webhook
   * @param {string} workflowId - The n8n webhook UUID
   * @param {object} payload - The data to pass to the workflow
   */
  async triggerWorkflow(workflowId, payload) {
    console.log(`[n8n] Triggering workflow: ${workflowId}`);
    try {
      // Assuming Sentience backend proxies to n8n to avoid exposing raw webhook URLs on client
      return await apiClient.post(`/workflows/${workflowId}/execute`, payload);
    } catch (error) {
      console.error(`[n8n] Failed to trigger workflow ${workflowId}`, error);
      throw error;
    }
  },

  /**
   * Fetches the status of a currently running n8n execution
   */
  async getExecutionStatus(executionId) {
    try {
      return await apiClient.get(`/workflows/execution/${executionId}`);
    } catch (error) {
      console.error(`[n8n] Failed to get execution status`, error);
      throw error;
    }
  }
};
