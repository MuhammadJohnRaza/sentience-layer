import { useState, useCallback } from 'react';

export function useWorkflow() {
  const [activeWorkflows, setActiveWorkflows] = useState([
    { id: 'wf_1', name: 'Global Optimization', progress: 0.74, status: 'running' },
    { id: 'wf_2', name: 'Threat Mitigation', progress: 1.0, status: 'completed' }
  ]);

  const startWorkflow = useCallback((name) => {
    const newWf = { id: `wf_${Date.now()}`, name, progress: 0, status: 'starting' };
    setActiveWorkflows(prev => [newWf, ...prev]);
    
    // Simulate progress
    let prog = 0;
    const interval = setInterval(() => {
      prog += 0.1;
      setActiveWorkflows(prev => prev.map(w => 
        w.id === newWf.id 
          ? { ...w, progress: Math.min(prog, 1), status: prog >= 1 ? 'completed' : 'running' } 
          : w
      ));
      if (prog >= 1) clearInterval(interval);
    }, 1000);
  }, []);

  const pauseWorkflow = useCallback((id) => {
    setActiveWorkflows(prev => prev.map(w => w.id === id ? { ...w, status: 'paused' } : w));
  }, []);

  return { activeWorkflows, startWorkflow, pauseWorkflow };
}
