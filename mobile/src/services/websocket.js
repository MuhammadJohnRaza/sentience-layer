export class WebSocketService {
  constructor(url) {
    this.url = url || (process.env.EXPO_PUBLIC_API_URL ? process.env.EXPO_PUBLIC_API_URL.replace('http', 'ws').replace('/api', '/ws') : 'ws://localhost:8000/ws');
    this.ws = null;
    this.listeners = new Set();
    this.reconnectAttempts = 0;
    this.maxReconnects = 5;
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('[WS Service] Connected to Sentience Kernel');
        this.reconnectAttempts = 0;
        this.notifyListeners({ type: 'CONNECTION_STATE', payload: 'CONNECTED' });
      };

      this.ws.onmessage = (event) => {
        let data;
        try {
          data = JSON.parse(event.data);
        } catch {
          data = { type: 'RAW_TEXT', payload: event.data };
        }
        this.notifyListeners(data);
      };

      this.ws.onclose = () => {
        console.log('[WS Service] Disconnected');
        this.notifyListeners({ type: 'CONNECTION_STATE', payload: 'DISCONNECTED' });
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.warn('[WS Service] Error:', error.message);
      };

    } catch (error) {
      console.error('[WS Service] Connection failed', error);
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnects) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * (2 ** this.reconnectAttempts), 10000);
      console.log(`[WS Service] Reconnecting in ${delay}ms... (Attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('[WS Service] Max reconnect attempts reached.');
    }
  }

  send(payload) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(payload));
    } else {
      console.warn('[WS Service] Cannot send, not connected');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback); // Returns unsubscribe function
  }

  notifyListeners(data) {
    this.listeners.forEach(listener => listener(data));
  }
}

// Export a singleton instance for global app usage
export const wsService = new WebSocketService();
