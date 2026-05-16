/**
 * WebSocket Client for Real-time Updates
 */

import { WS_URL } from "./constants";
import { WebSocketMessage } from "@/types";

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private listeners: Map<string, Set<(msg: any) => void>> = new Map();
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket(WS_URL);

    this.ws.onopen = () => {
      console.log("WebSocket connected");
      this.reconnectAttempts = 0;
      this.emit("system", { type: "connected" });
    };

    this.ws.onmessage = (event) => {
      try {
        const msg: WebSocketMessage = JSON.parse(event.data);
        this.emit(msg.type, msg.payload);
      } catch (e) {
        console.error("WebSocket message parse error:", e);
      }
    };

    this.ws.onclose = () => {
      this.emit("system", { type: "disconnected" });
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.emit("system", { type: "error", error });
    };
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.ws?.close();
    this.ws = null;
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max reconnection attempts reached");
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30000);

    this.reconnectTimer = setTimeout(() => {
      console.log(`Reconnecting... attempt ${this.reconnectAttempts}`);
      this.connect();
    }, delay);
  }

  send(type: string, payload: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload, timestamp: new Date().toISOString() }));
    }
  }

  on(event: string, callback: (msg: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    return () => this.off(event, callback);
  }

  off(event: string, callback: (msg: any) => void) {
    this.listeners.get(event)?.delete(callback);
  }

  private emit(event: string, payload: any) {
    this.listeners.get(event)?.forEach((cb) => {
      try {
        cb(payload);
      } catch (e) {
        console.error("Listener error:", e);
      }
    });
  }
}

export const wsClient = new WebSocketClient();