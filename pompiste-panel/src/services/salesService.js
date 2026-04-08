import api from './api';

export const getSales = (params) => api.get('/sales/', { params });
export const createSale = (data) => api.post('/sales/', data);
export const getFuelPrices = () => api.get('/sales/prices/');
