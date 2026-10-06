import axios from 'axios';

const baseURL = process.env.VUE_APP_API_BASE_URL || '/api';
if (process.env.NODE_ENV === 'production' && /^http:\/\//i.test(baseURL)) {
  throw new Error('Production API URLs must use HTTPS or a same-origin path.');
}

const api = axios.create({
  baseURL,
});

export default api;