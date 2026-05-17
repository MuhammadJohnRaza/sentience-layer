import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import chatReducer from './chatSlice';
import dashboardReducer from './dashboardSlice';
import workflowReducer from './workflowSlice';
import actionsReducer from './actionsSlice';
import settingsReducer from './settingsSlice';
import simulationReducer from './simulationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    chat: chatReducer,
    dashboard: dashboardReducer,
    workflow: workflowReducer,
    actions: actionsReducer,
    settings: settingsReducer,
    simulation: simulationReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // Useful when dealing with complex non-serializable payloads or WS instances if needed
    }),
});

export default store;
