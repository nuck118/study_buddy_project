import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const BACKEND_URL = process.env.BACKEND_URL || 'http://192.168.0.54:8000';

async function getAccessToken() {
  return await SecureStore.getItemAsync('accessToken');
}

async function getRefreshToken() {
  return await SecureStore.getItemAsync('refreshToken');
}

async function setTokens(access, refresh) {
  if (access) await SecureStore.setItemAsync('accessToken', access);
  if (refresh) await SecureStore.setItemAsync('refreshToken', refresh);
}

async function clearTokens() {
  await SecureStore.deleteItemAsync('accessToken');
  await SecureStore.deleteItemAsync('refreshToken');
}

const api = axios.create({
  baseURL: `${BACKEND_URL}/api/`,
  timeout: 15000,
});

// Request interceptor: attach access token
api.interceptors.request.use(async config => {
  const token = await getAccessToken();
  if (token) {
    config.headers = { ...(config.headers || {}), Authorization: `Bearer ${token}` };
  }
  return config;
}, err => Promise.reject(err));

// Response interceptor: handle 401 and refresh
let isRefreshing = false;
let refreshQueue = [];

async function processQueue(error, token = null) {
  refreshQueue.forEach(p => {
    if (error) p.reject(error);
    else p.resolve(token);
  });
  refreshQueue = [];
}

api.interceptors.response.use(response => response, async error => {
  const originalRequest = error.config;
  if (error.response && error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({ resolve, reject });
      }).then(token => {
        originalRequest.headers['Authorization'] = `Bearer ${token}`;
        return axios(originalRequest);
      }).catch(e => Promise.reject(e));
    }

    isRefreshing = true;
    const refresh = await getRefreshToken();
    if (!refresh) {
      await clearTokens();
      isRefreshing = false;
      return Promise.reject(error);
    }

    try {
      const resp = await axios.post(`${BACKEND_URL}/api/token/refresh/`, { refresh });
      const newAccess = resp.data.access;
      const newRefresh = resp.data.refresh || refresh;
      await setTokens(newAccess, newRefresh);
      processQueue(null, newAccess);
      originalRequest.headers['Authorization'] = `Bearer ${newAccess}`;
      return axios(originalRequest);
    } catch (e) {
      processQueue(e, null);
      await clearTokens();
      return Promise.reject(e);
    } finally {
      isRefreshing = false;
    }
  }
  return Promise.reject(error);
});

// Convenience API methods
export async function get(path, config) {
  return api.get(path, config);
}

export async function post(path, data, config) {
  return api.post(path, data, config);
}

export async function put(path, data, config) {
  return api.put(path, data, config);
}

export async function del(path, config) {
  return api.delete(path, config);
}

export async function loginWithGoogle(id_token) {
  const resp = await axios.post(`${BACKEND_URL}/api/auth/google/`, { id_token });
  const { access, refresh } = resp.data;
  await setTokens(access, refresh);
  return resp.data;
}

export async function logout() {
  await clearTokens();
}

export default api;
