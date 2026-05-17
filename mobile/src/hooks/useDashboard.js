import { useState, useEffect } from 'react';

export function useDashboard() {
  const [metrics, setMetrics] = useState({
    systemHealth: 98,
    activeAgents: 18,
    latentThreads: 1042,
    threatLevel: 'LOW',
    uptime: 99.9
  });

  // Simulate real-time dashboard updates
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        latentThreads: prev.latentThreads + Math.floor(Math.random() * 10) - 5,
        uptime: Math.min(100, prev.uptime + (Math.random() > 0.8 ? 0.01 : 0))
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return { metrics };
}
