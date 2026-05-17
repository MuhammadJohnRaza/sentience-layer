/** * WebSocket connection hook */
import { useEffect, useState, useCallback } from "react";
import { wsClient } from "@/lib/websocket";
export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(true);
  useEffect(() => {
    wsClient.connect();
    const unsubConnect = wsClient.on("system", (payload) => {
      if (payload.type === "connected") setIsConnected(true);
      if (payload.type === "disconnected") setIsConnected(false);
    });
    return () => {
      unsubConnect();
      wsClient.disconnect();
    };
  }, []);
  const send = useCallback((type: string, payload: any) => {
    wsClient.send(type, payload);
  }, []);
  const subscribe = useCallback(
    (event: string, callback: (msg: any) => void) => {
      return wsClient.on(event, callback);
    },
    [],
  );
  return {
    isConnected,
    send,
    subscribe,
  };
}
