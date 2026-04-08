import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import salesReducer from './salesSlice';
import shiftReducer from './shiftSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    sales: salesReducer,
    shift: shiftReducer,
  },
});

export default store;
