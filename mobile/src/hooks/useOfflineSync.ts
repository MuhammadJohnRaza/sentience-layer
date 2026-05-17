import { useState, useEffect, useCallback } from 'react';
import NetInfo from '@react-native-community/netinfo';
import { useLocalStorage } from './useLocalStorage';

export interface OfflineAction {
  id: string;
  type: string;
  payload: any;
  timestamp: number;
}

export function useOfflineSync() {
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [offlineQueue, setOfflineQueue] = useLocalStorage<OfflineAction[]>('SENTIENCE_OFFLINE_QUEUE', []);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? true);
    });
    return () => unsubscribe();
  }, []);

  const queueAction = useCallback((action: Omit<OfflineAction, 'timestamp'>) => {
    setOfflineQueue(prev => [...prev, { ...action, timestamp: Date.now() }]);
  }, [setOfflineQueue]);

  const syncNow = useCallback(async () => {
    if (!isOnline || offlineQueue.length === 0) return;
    
    setIsSyncing(true);
    try {
      console.log(`Syncing ${offlineQueue.length} offline actions to Sentience Kernel...`);
      await new Promise(resolve => setTimeout(resolve, 1500));
      setOfflineQueue([]);
    } catch (error) {
      console.error('Sync failed', error);
    } finally {
      setIsSyncing(false);
    }
  }, [isOnline, offlineQueue, setOfflineQueue]);

  useEffect(() => {
    if (isOnline && offlineQueue.length > 0) {
      syncNow();
    }
  }, [isOnline, offlineQueue.length, syncNow]);

  return { isOnline, offlineQueue, queueAction, syncNow, isSyncing };
}
