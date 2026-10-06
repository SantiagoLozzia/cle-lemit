import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? 'http://192.168.100.10:8000/api' : '/api',
});

export default api;