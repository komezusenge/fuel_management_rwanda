import api from './api';

export const login = (credentials) => api.post('/auth/login/', credentials);
export const logout = () => api.post('/auth/logout/');
export const refreshToken = (refresh) => api.post('/auth/refresh/', { refresh });
export const getCurrentUser = () => api.get('/users/me/');
