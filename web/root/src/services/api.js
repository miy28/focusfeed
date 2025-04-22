const BASE = import.meta.env.MODE === 'production' ? '' : '/api'

export async function fetchFeed(query = 'SpaceX') {
  const res = await fetch(`${BASE}/feed?query=${encodeURIComponent(query)}`)
  return res.json()
}

export async function touchDB(word) {
  const res = await fetch(`${BASE}/touch_db`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word }),
  })
  return res.json()
}
