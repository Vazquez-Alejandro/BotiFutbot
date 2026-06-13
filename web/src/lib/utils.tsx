import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Loader2 } from 'lucide-react'
import { apiGet } from '@/lib/api'

const ADS = [
  {
    name: 'Bet365',
    text: '🎲 Apostá en los mejores partidos con Bet365',
    url: 'https://www.bet365.com',
    bg: 'from-green-600 to-green-800',
  },
  {
    name: 'Betano',
    text: '🔥 Cuotas en vivo y los mejores bonus en Betano',
    url: 'https://www.betano.com',
    bg: 'from-yellow-600 to-yellow-800',
  },
  {
    name: 'Sportingbet',
    text: '⚽ Tradición en apuestas deportivas — Sportingbet',
    url: 'https://sportingbet.com',
    bg: 'from-blue-600 to-blue-800',
  },
]

export function AdBanner() {
  const ad = ADS[Math.floor(Math.random() * ADS.length)]

  return (
    <a
      href={ad.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`block bg-gradient-to-r ${ad.bg} rounded-xl p-4 text-white hover:opacity-90 transition mb-6`}
    >
      <p className="text-sm font-medium">{ad.text}</p>
    </a>
  )
}

export function useLiveMatches() {
  const [matches, setMatches] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = () => {
      apiGet('/api/leagues/live')
        .then(data => setMatches(data.matches || []))
        .catch(() => setMatches([]))
        .finally(() => setLoading(false))
    }
    fetch()
    const interval = setInterval(fetch, 30000)
    return () => clearInterval(interval)
  }, [])

  return { matches, loading }
}

export function formatTime(iso: string) {
  const d = new Date(iso)
  return d.toLocaleString('es-AR', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
  })
}
