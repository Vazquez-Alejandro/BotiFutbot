const API_URL = 'https://botifutbol-api.onrender.com/api';

export async function fetchStandings() {
  const res = await fetch(`${API_URL}/mundial/standings`);
  const data = await res.json();
  return data.groups || [];
}

export async function fetchFixtures() {
  const res = await fetch(`${API_URL}/mundial/fixtures`);
  const data = await res.json();
  return data.fixtures || [];
}
