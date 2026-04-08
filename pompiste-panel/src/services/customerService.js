import api from './api';

export const getCustomers = (params) => api.get('/customers/', { params });
export const createCreditTransaction = (data) => api.post('/customers/transactions/', data);
