export const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000/api';

export const apiClient = {
  async get(endpoint) {
    try {
      const response = await fetch(`${API_URL}${endpoint}`);
      if (!response.ok) throw new Error(`GET request failed: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('[API GET Error]:', error);
      throw error;
    }
  },

  async post(endpoint, data) {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error(`POST request failed: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('[API POST Error]:', error);
      throw error;
    }
  }
};
