import axios from "axios";

// Point this to your running Nebula API
const API_BASE = "http://127.0.0.1:8000";

export async function fetchCards(filters = {}) {
  const params = new URLSearchParams(filters).toString();
  const response = await axios.get(`${API_BASE}/cards?${params}`);
  return response.data;
}

export async function fetchCard(number) {
  const response = await axios.get(`${API_BASE}/cards/${number}`);
  return response.data;
}

export async function searchCards(q) {
  const response = await axios.get(`${API_BASE}/search?q=${q}`);
  return response.data;
}

export async function fetchStats() {
  const response = await axios.get(`${API_BASE}/stats`);
  return response.data;
}
