import { createSlice } from '@reduxjs/toolkit';

const stored = JSON.parse(localStorage.getItem('auth') || 'null');

const initialState = {
  user: stored?.user || null,
  accessToken: stored?.accessToken || null,
  refreshToken: stored?.refreshToken || null,
  isAuthenticated: !!stored?.accessToken,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart(state) {
      state.loading = true;
      state.error = null;
    },
    loginSuccess(state, action) {
      const { user, access, refresh } = action.payload;
      state.user = user;
      state.accessToken = access;
      state.refreshToken = refresh;
      state.isAuthenticated = true;
      state.loading = false;
      state.error = null;
      localStorage.setItem('auth', JSON.stringify({ user, accessToken: access, refreshToken: refresh }));
    },
    loginFailure(state, action) {
      state.loading = false;
      state.error = action.payload;
    },
    logout(state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.error = null;
      localStorage.removeItem('auth');
    },
    tokenRefreshed(state, action) {
      state.accessToken = action.payload;
      const auth = JSON.parse(localStorage.getItem('auth') || '{}');
      auth.accessToken = action.payload;
      localStorage.setItem('auth', JSON.stringify(auth));
    },
  },
});

export const { loginStart, loginSuccess, loginFailure, logout, tokenRefreshed } = authSlice.actions;
export default authSlice.reducer;
