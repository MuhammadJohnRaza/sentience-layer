import { useState, useCallback } from 'react';

export function useSimulation() {
  const [simulations, setSimulations] = useState([
    { id: '1', scenarioName: 'Q3 User Acquisition Spike', probability: 0.84, branchesExplored: 1048576, status: 'success' },
    { id: '2', scenarioName: 'Server Subsystem Failure', probability: 0.12, branchesExplored: 524288, status: 'fail' }
  ]);
  const [isRunning, setIsRunning] = useState(false);

  const runSimulation = useCallback(async (scenarioName) => {
    setIsRunning(true);
    
    // Simulate Monte Carlo compute delay
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    const newSim = {
      id: Date.now().toString(),
      scenarioName,
      probability: Number((Math.random() * 0.9 + 0.1).toFixed(2)),
      branchesExplored: Math.floor(Math.random() * 5000000) + 100000,
      status: Math.random() > 0.3 ? 'success' : 'fail'
    };
    
    setSimulations(prev => [newSim, ...prev]);
    setIsRunning(false);
    return newSim;
  }, []);

  return { simulations, isRunning, runSimulation };
}
