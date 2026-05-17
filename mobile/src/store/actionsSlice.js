import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  pendingActions: [
    { id: 'act_1', type: 'deploy', title: 'Deploy Server Upgrades', status: 'pending' },
    { id: 'act_2', type: 'hedge', title: 'Execute Market Hedge', status: 'pending' },
    { id: 'act_3', type: 'security', title: 'Quarantine Sub-Network', status: 'pending' }
  ],
  approvedActions: [],
  rejectedActions: [],
};

const actionsSlice = createSlice({
  name: 'actions',
  initialState,
  reducers: {
    approveAction: (state, action) => {
      const act = state.pendingActions.find(a => a.id === action.payload);
      if (act) {
        state.pendingActions = state.pendingActions.filter(a => a.id !== action.payload);
        state.approvedActions.push({ ...act, status: 'approved' });
      }
    },
    rejectAction: (state, action) => {
      const act = state.pendingActions.find(a => a.id === action.payload);
      if (act) {
        state.pendingActions = state.pendingActions.filter(a => a.id !== action.payload);
        state.rejectedActions.push({ ...act, status: 'rejected' });
      }
    },
    addPendingAction: (state, action) => {
      state.pendingActions.push(action.payload);
    }
  }
});

export const { approveAction, rejectAction, addPendingAction } = actionsSlice.actions;
export default actionsSlice.reducer;
