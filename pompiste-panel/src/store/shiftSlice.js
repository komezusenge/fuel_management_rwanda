import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentShift: null,
  shifts: [],
  loading: false,
  error: null,
};

const shiftSlice = createSlice({
  name: 'shift',
  initialState,
  reducers: {
    setCurrentShift(state, action) {
      state.currentShift = action.payload;
    },
    setShifts(state, action) {
      state.shifts = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    setError(state, action) {
      state.error = action.payload;
    },
    clearCurrentShift(state) {
      state.currentShift = null;
    },
  },
});

export const { setCurrentShift, setShifts, setLoading, setError, clearCurrentShift } = shiftSlice.actions;
export default shiftSlice.reducer;
