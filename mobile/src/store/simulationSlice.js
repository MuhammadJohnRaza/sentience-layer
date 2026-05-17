import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  history: [
    { id: 'sim_1', scenarioName: 'Q3 User Acquisition Spike', probability: 0.84, branchesExplored: 1048576, status: 'success' },
    { id: 'sim_2', scenarioName: 'Server Subsystem Failure', probability: 0.12, branchesExplored: 524288, status: 'fail' }
  ],
  isRunning: false,
};

const simulationSlice = createSlice({
  name: 'simulation',
  initialState,
  reducers: {
    startSimulation: (state) => {
      state.isRunning = true;
    },
    finishSimulation: (state, action) => {
      state.isRunning = false;
      state.history.unshift(action.payload);
    },
    clearSimulationHistory: (state) => {
      state.history = [];
    }
  }
});

export const { startSimulation, finishSimulation, clearSimulationHistory } = simulationSlice.actions;
export default simulationSlice.reducer;
