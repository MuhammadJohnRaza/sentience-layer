import { useState, useEffect, useCallback } from 'react';
import NetInfo from '@react-native-community/netinfo';
import { useLocalStorage } from './useLocalStorage';

export function useOfflineSync() {
  const [isOnline, setIsOnline] = useState(true);
  const [offlineQueue, setOfflineQueue] = useLocalStorage('SENTIENCE_OFFLINE_QUEUE', []);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? true);
    });
    return () => unsubscribe();
  }, []);

  const queueAction = useCallback((action) => {
    setOfflineQueue(prev => [...prev, { ...action, timestamp: Date.now() }]);
  }, [setOfflineQueue]);

  const syncNow = useCallback(async () => {
    if (!isOnline || offlineQueue.length === 0) return;
    
    setIsSyncing(true);
    try {
      // Simulate API sync push
      console.log(`Syncing ${offlineQueue.length} offline actions to Sentience Kernel...`);
      await new Promise(resolve => setTimeout(resolve, 1500));
      setOfflineQueue([]); // Clear on success
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
