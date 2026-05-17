import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: null,
  isAuthenticated: false,
  guestMode: true,
  token: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
      state.guestMode = false;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      state.guestMode = true;
    },
    setGuestMode: (state) => {
      state.guestMode = true;
      state.isAuthenticated = false;
    }
  }
});

export const { login, logout, setGuestMode } = authSlice.actions;
export default authSlice.reducer;
