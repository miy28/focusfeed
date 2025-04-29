import React, { useEffect, useState } from 'react'
// #import { fetchFeed, touchDB } from './services/api.js'


async function fetchFeed(query) {
  const res = await fetch(`/api/feed?query=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function touchDB(word) {
  const res = await fetch(`/api/touch_db`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();  // { result: "…" }
}

// Sample feed notes for layout demonstration
const sampleFeed = [
  {
    title: "Apple Unveils New M4 Chip",
    content: "Apple's latest M4 processor promises up to 50% faster performance compared to its predecessor, with improved power efficiency for mobile devices...",
    url: "https://example.com/apple-m4-announcement",
    source: "TechCrunch"
  },
  {
    title: "Global Summit on Climate Change Begins",
    content: "World leaders gather in Geneva to discuss actionable strategies aimed at reducing carbon emissions by 2030 and beyond...",
    url: "https://example.com/climate-summit-2025",
    source: "BBC News"
  },
  {
    title: "Breakthrough in Fusion Energy",
    content: "Scientists at the National Lab report a net-positive energy output from their latest fusion reactor test, marking a historic milestone...",
    url: "https://example.com/fusion-energy-milestone",
    source: "Science Daily"
  },
  {
    title: "Historic Mars Rover Landing Success",
    content: "NASA's new rover \"Mars Explorer\" has successfully touched down, sending back high-resolution images and data on Martian terrain...",
    url: "https://example.com/mars-rover-landing",
    source: "NASA"
  }
]

// Centralized inline styles
const styles = {
  app: {
    minHeight: '100vh',
    width: '100vw',
    background: 'linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%)',
    color: '#f0f0f0',
    display: 'flex',
    flexDirection: 'column',
    fontFamily: 'system-ui, Avenir, Helvetica, Arial, sans-serif',
  },
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 2rem',
    background: 'rgba(0, 0, 0, 0.4)',
    backdropFilter: 'blur(8px)',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
  },
  navBrand: {
    fontSize: '2rem',
    fontWeight: 700,
    letterSpacing: '1px',
  },
  navList: {
    display: 'flex',
    gap: '1.5rem',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  },
  navItem: {
    cursor: 'pointer',
    position: 'relative',
    paddingBottom: '4px',
    transition: 'color 0.3s, box-shadow 0.3s',
  },
  navItemHover: {
    color: '#FFD700',
    boxShadow: 'inset 0 -2px 0 #FFD700',
  },
  navItemActive: {
    color: '#FF8C00',
    boxShadow: 'inset 0 -2px 0 #FF8C00',
  },
  main: {
    flex: 1,
    width: '100%',
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '2rem',
    boxSizing: 'border-box',
  },
  controls: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '1rem',
    marginBottom: '2rem',
    alignItems: 'center',
  },
  input: {
    flex: '1 1 250px',
    padding: '0.75rem 1rem',
    borderRadius: '30px',
    border: 'none',
    fontSize: '1rem',
    outline: 'none',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
    backgroundColor: 'rgba(0,0,0,0.2)',
    color: '#fff',
  },
  button: {
    padding: '0.75rem 1.5rem',
    borderRadius: '30px',
    border: 'none',
    fontSize: '1rem',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.3s, transform 0.2s',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
  },
  cardGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '2rem',
  },
  card: {
    background: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '12px',
    padding: '1.5rem',
    display: 'flex',
    flexDirection: 'column',
    backdropFilter: 'blur(10px)',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
    transition: 'transform 0.3s, box-shadow 0.3s',
  },
  cardHover: {
    transform: 'translateY(-8px)',
    boxShadow: '0 8px 40px rgba(0, 0, 0, 0.4)',
  },
  cardTitle: {
    margin: '0 0 0.75rem',
    fontSize: '1.3rem',
    fontWeight: 700,
    lineHeight: '1.2',
  },
  cardContent: {
    flex: 1,
    fontSize: '1rem',
    marginBottom: '1.25rem',
    lineHeight: '1.4',
  },
  cardFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '0.85rem',
  },
  link: {
    color: '#FFD700',
    textDecoration: 'none',
    fontWeight: 600,
    transition: 'color 0.3s',
  }
}

// Navbar supports hover and active state
function Navbar({ current, onSelect }) {
  const [hovered, setHovered] = useState(null)
  const items = ['Home', 'Trending Topics', 'My Feed', 'Account']

  return (
    <header style={styles.navbar}>
      <div style={styles.navBrand}>FocusFeed</div>
      <ul style={styles.navList}>
        {items.map((item, idx) => {
          const isActive = current === item
          const isHovered = hovered === idx
          return (
            <li
              key={item}
              style={{
                ...styles.navItem,
                ...(isActive ? styles.navItemActive : {}),
                ...(isHovered && !isActive ? styles.navItemHover : {}),
              }}
              onClick={() => onSelect(item)}
              onMouseEnter={() => setHovered(idx)}
              onMouseLeave={() => setHovered(null)}
            >
              {item}
            </li>
          )
        })}
      </ul>
    </header>
  )
}

export default function App() {
  const [page, setPage] = useState('Home')
  const [query, setQuery] = useState('SpaceX')
  const [feed, setFeed] = useState([])
  const [msg, setMsg] = useState('')
  const [hoverCard, setHoverCard] = useState(null)

  useEffect(() => {
    if (page === 'Home') load()
  }, [page])

  async function load(q = query) {
    setMsg('Loading…')
    try {
      const data = await fetchFeed(q)
      setFeed(data)
      setMsg('')
    } catch {
      setMsg('Error fetching data')
    }
  }

  function renderPage() {
    switch (page) {
      case 'Home': {
        const display = feed.length > 0 ? feed : sampleFeed
        return (
          <>
            <div style={styles.controls}>
              <input
                style={styles.input}
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search topics..."
              />
              <button
                style={{ ...styles.button, backgroundColor: '#FFD700', color: '#333' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.05)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                onClick={() => load()}
              >Search</button>
              <button
                style={{ ...styles.button, backgroundColor: '#4CAF50', color: '#fff' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.05)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                onClick={async () => setMsg((await touchDB(query)).result)}
              >Generate FeedNote</button>
            </div>
            {msg && <p style={{ fontStyle: 'italic', marginBottom: '1.5rem' }}>{msg}</p>}
            <section style={styles.cardGrid}>
              {display.map((n, idx) => (
                <article
                  key={idx}
                  style={{
                    ...styles.card,
                    ...(hoverCard === idx ? styles.cardHover : {}),
                  }}
                  onMouseEnter={() => setHoverCard(idx)}
                  onMouseLeave={() => setHoverCard(null)}
                >
                  <h3 style={styles.cardTitle}>{n.title}</h3>
                  <p style={styles.cardContent}>{n.content}</p>
                  <div style={styles.cardFooter}>
                    <span style={{ opacity: 0.8 }}>{n.source}</span>
                    <a href={n.url} target="_blank" rel="noopener noreferrer" style={styles.link}>
                      Read →
                    </a>
                  </div>
                </article>
              ))}
            </section>
          </>
        )
      }
      case 'Trending Topics': {
        const trending = ['AI Revolution', 'Global Climate', 'Tech Stocks', 'Space Exploration']
        return (
          <section style={styles.cardGrid}>
            {trending.map((t, idx) => (
              <article key={idx} style={styles.card}>
                <h3 style={styles.cardTitle}>{t}</h3>
              </article>
            ))}
          </section>
        )
      }
      case 'My Feed': {
        return (
          <section style={styles.cardGrid}>
            <article style={styles.card}>
              <h3 style={styles.cardTitle}>Your Feed</h3>
              <p style={styles.cardContent}>No items yet—follow topics to populate your personal feed!</p>
            </article>
          </section>
        )
      }
      case 'Account': {
        return (
          <section style={styles.cardGrid}>
            <article style={styles.card}>
              <h3 style={styles.cardTitle}>Account Settings</h3>
              <button
                style={{ ...styles.button, backgroundColor: '#FF6347', color: '#fff' }}
                onClick={() => alert('Logged out (dummy)')}
              >Log Out</button>
            </article>
          </section>
        )
      }
      default:
        return null
    }
  }

  return (
    <div style={styles.app}>
      <Navbar current={page} onSelect={setPage} />
      <main style={styles.main}>{renderPage()}</main>
    </div>
  )
}
// copilot comm
// This is a simple React app that fetches and displays a feed of articles based on a search query.
// It includes a navbar, a search input, and buttons to generate a feed note.
// The app uses a unified style for all components, including hover effects and responsive design.
// The Navbar component has a hover effect for menu items.
// The main App component manages the state of the query, feed, and messages.
// It fetches data from an API and displays it in a grid of cards.
// The cards have hover effects and display the article title, content, source, and a link to read more.
// The app is styled using inline styles for simplicity and consistency.
