import { createSlice } from '@reduxjs/toolkit';

const OFFLINE_KEY = 'offline_sales_queue';

const initialState = {
  sales: [],
  prices: {},
  loading: false,
  error: null,
  offlineQueue: JSON.parse(localStorage.getItem(OFFLINE_KEY) || '[]'),
};

const salesSlice = createSlice({
  name: 'sales',
  initialState,
  reducers: {
    setSales(state, action) {
      state.sales = action.payload;
    },
    addSale(state, action) {
      state.sales.unshift(action.payload);
    },
    setPrices(state, action) {
      state.prices = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    setError(state, action) {
      state.error = action.payload;
    },
    enqueueOfflineSale(state, action) {
      state.offlineQueue.push(action.payload);
      localStorage.setItem(OFFLINE_KEY, JSON.stringify(state.offlineQueue));
    },
    removeOfflineSale(state, action) {
      state.offlineQueue = state.offlineQueue.filter((_, i) => i !== action.payload);
      localStorage.setItem(OFFLINE_KEY, JSON.stringify(state.offlineQueue));
    },
    clearOfflineQueue(state) {
      state.offlineQueue = [];
      localStorage.removeItem(OFFLINE_KEY);
    },
  },
});

export const {
  setSales,
  addSale,
  setPrices,
  setLoading,
  setError,
  enqueueOfflineSale,
  removeOfflineSale,
  clearOfflineQueue,
} = salesSlice.actions;
export default salesSlice.reducer;
