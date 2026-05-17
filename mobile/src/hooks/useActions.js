import { useState, useCallback } from 'react';

export function useActions() {
  const [actions, setActions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchActions = useCallback(async () => {
    setIsLoading(true);
    // Simulate API fetch
    setTimeout(() => {
      setActions([
        { id: 1, type: 'deploy', title: 'Deploy Server Upgrades', status: 'pending' },
        { id: 2, type: 'hedge', title: 'Execute Market Hedge', status: 'pending' },
        { id: 3, type: 'security', title: 'Quarantine Sub-Network', status: 'pending' }
      ]);
      setIsLoading(false);
    }, 600);
  }, []);

  const approveAction = useCallback((id) => {
    setActions(prev => prev.map(a => a.id === id ? { ...a, status: 'approved' } : a));
  }, []);

  const rejectAction = useCallback((id) => {
    setActions(prev => prev.filter(a => a.id !== id));
  }, []);

  return { actions, isLoading, fetchActions, approveAction, rejectAction };
}
