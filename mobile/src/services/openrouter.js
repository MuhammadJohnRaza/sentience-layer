import { apiClient } from './api';

export const openRouterService = {
  /**
   * Proxies a prompt request through the backend to OpenRouter
   * @param {string} prompt - User or system prompt
   * @param {string} model - Preferred model (e.g. 'google/gemini-2.5-flash:free')
   */
  async sendPrompt(prompt, model = 'google/gemini-2.5-flash:free') {
    console.log(`[OpenRouter] Dispatching prompt to ${model}`);
    try {
      const response = await apiClient.post('/llm/chat', { prompt, model });
      return response.data;
    } catch (error) {
      console.error('[OpenRouter] Prompt dispatch failed', error);
      throw error;
    }
  },

  /**
   * Fetches available models from OpenRouter via backend cache
   */
  async getAvailableModels() {
    try {
      return await apiClient.get('/llm/models');
    } catch (error) {
      console.error('[OpenRouter] Failed to fetch models', error);
      return [];
    }
  }
};
