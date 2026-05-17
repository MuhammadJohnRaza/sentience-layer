import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  offlineSyncEnabled: true,
  stealthModeEnabled: false,
  computeBoostEnabled: true,
  theme: 'dark', // Fixed to dark for Sentience
};

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    toggleOfflineSync: (state) => {
      state.offlineSyncEnabled = !state.offlineSyncEnabled;
    },
    toggleStealthMode: (state) => {
      state.stealthModeEnabled = !state.stealthModeEnabled;
    },
    toggleComputeBoost: (state) => {
      state.computeBoostEnabled = !state.computeBoostEnabled;
    }
  }
});

export const { toggleOfflineSync, toggleStealthMode, toggleComputeBoost } = settingsSlice.actions;
export default settingsSlice.reducer;
