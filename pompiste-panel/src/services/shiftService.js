import api from './api';

export const getShifts = (params) => api.get('/pumps/shifts/', { params });
export const getCurrentShift = () => api.get('/pumps/shifts/current/');
export const openShift = (data) => api.post('/pumps/shifts/', data);
export const closeShift = (id, data) => api.post(`/pumps/shifts/${id}/close/`, data);
