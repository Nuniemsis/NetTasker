import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Replace with your FastAPI backend URL
});

export const createTask = () => api.post('/tasks');
export const getTasks = (limit = 10, offset = 0) => {
  return api.get(`/tasks`, { params: { limit, offset } });
};

export const getTaskCount = (status) => {
  return api.get(`/tasks/count`, { params: { status } });
};