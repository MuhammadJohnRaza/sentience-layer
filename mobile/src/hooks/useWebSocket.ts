import { useState, useEffect, useCallback, useRef } from 'react';

export interface WebSocketMessage {
  type: string;
  payload: any;
  timestamp?: number;
}

export function useWebSocket(url: string = 'ws://localhost:8000/ws') {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const ws = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log('Sentience Kernel WS Connected');
        setIsConnected(true);
      };

      ws.current.onmessage = (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data) as WebSocketMessage;
          setLastMessage(data);
        } catch (err) {
          // Fallback if not valid JSON
          setLastMessage({ type: 'UNKNOWN', payload: e.data });
        }
      };

      ws.current.onerror = (e: Event) => {
        console.warn('Sentience WS Error:', e);
      };

      ws.current.onclose = () => {
        console.log('Sentience Kernel WS Disconnected');
        setIsConnected(false);
      };
    } catch (error) {
      console.error('Failed to instantiate WebSocket', error);
    }
  }, [url]);

  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
    }
  }, []);

  const sendMessage = useCallback((msg: WebSocketMessage | string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } else {
      console.warn('Cannot send message. WS not connected.');
    }
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return { isConnected, lastMessage, sendMessage, reconnect: connect };
}
