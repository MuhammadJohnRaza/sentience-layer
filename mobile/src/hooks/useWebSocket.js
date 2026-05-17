import { useState, useEffect, useCallback, useRef } from 'react';

export function useWebSocket(url = 'ws://localhost:3000/ws') {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log('Sentience Kernel WS Connected');
        setIsConnected(true);
      };

      ws.current.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);
          setLastMessage(data);
        } catch (err) {
          setLastMessage(e.data);
        }
      };

      ws.current.onerror = (e) => {
        console.warn('Sentience WS Error:', e.message);
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

  const sendMessage = useCallback((msg) => {
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
