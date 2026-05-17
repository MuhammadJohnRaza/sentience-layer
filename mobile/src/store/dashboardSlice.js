import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  metrics: {
    systemHealth: 98,
    activeAgents: 18,
    latentThreads: 1042,
    threatLevel: 'LOW',
    uptime: 99.9
  },
  recentActivity: [
    { id: 1, text: 'Swarm successfully handled API spike.', type: 'info' },
    { id: 2, text: 'Economic yield target adjusted down.', type: 'warning' }
  ]
};

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    updateMetrics: (state, action) => {
      state.metrics = { ...state.metrics, ...action.payload };
    },
    addActivityLog: (state, action) => {
      state.recentActivity.unshift(action.payload);
      if (state.recentActivity.length > 50) {
        state.recentActivity.pop();
      }
    }
  }
});

export const { updateMetrics, addActivityLog } = dashboardSlice.actions;
export default dashboardSlice.reducer;
