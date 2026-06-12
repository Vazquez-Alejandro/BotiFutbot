'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Loader2, Clock, MapPin } from 'lucide-react'
import { apiGet } from '@/lib/api'
import { useParams } from 'next/navigation'

interface MatchDetail {
  id: number
  date: string
  status: string
  status_long: string
  elapsed: number | null
  venue: string
  referee: string
  home: { id: number; name: string; logo: string; winner: boolean | null }
  away: { id: number; name: string; logo: string; winner: boolean | null }
  goals: { home: number | null; away: number | null }
  events: Array<{
    time: number
    team: string
    player: string
    assist: string | null
    type: string
    detail: string
  }>
  statistics: any
}

export default function MatchPage() {
  const params = useParams()
  const fixtureId = params?.id
  const [match, setMatch] = useState<MatchDetail | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!fixtureId) return
    apiGet(`/api/leagues/match/${fixtureId}`)
      .then(data => setMatch(data.match))
      .catch(() => setMatch(null))
      .finally(() => setLoading(false))
  }, [fixtureId])

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
      </div>
    )
  }

  if (!match) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <p className="text-gray-500">Partido no encontrado</p>
      </div>
    )
  }

  const isLive = ['1H', '2H', 'HT', 'ET', 'P', 'LIVE'].includes(match.status)

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/fixture" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-lg font-bold text-white">Detalle del partido</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 mb-6">
          <div className="text-center text-gray-500 text-sm mb-4">
            {match.venue && (
              <span className="flex items-center justify-center gap-1">
                <MapPin className="w-3 h-3" /> {match.venue}
              </span>
            )}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex-1 text-center">
              {match.home.logo && <img src={match.home.logo} alt="" className="w-16 h-16 mx-auto mb-2" />}
              <p className="text-white font-semibold">{match.home.name}</p>
            </div>

            <div className="px-6">
              <div className="flex items-center gap-3">
                <span className={`text-4xl font-bold ${isLive ? 'text-primary' : 'text-white'}`}>
                  {match.goals.home ?? '-'}
                </span>
                <span className="text-gray-600 text-2xl">-</span>
                <span className={`text-4xl font-bold ${isLive ? 'text-primary' : 'text-white'}`}>
                  {match.goals.away ?? '-'}
                </span>
              </div>
              {isLive && match.elapsed && (
                <p className="text-primary text-center text-sm mt-1 animate-pulse">
                  {match.elapsed}'
                </p>
              )}
              {match.status === 'FT' && (
                <p className="text-gray-500 text-center text-sm mt-1">FINAL</p>
              )}
            </div>

            <div className="flex-1 text-center">
              {match.away.logo && <img src={match.away.logo} alt="" className="w-16 h-16 mx-auto mb-2" />}
              <p className="text-white font-semibold">{match.away.name}</p>
            </div>
          </div>
        </div>

        {match.events && match.events.length > 0 && (
          <div className="bg-dark-card border border-dark-border rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">Eventos</h2>
            <div className="space-y-3">
              {match.events.map((event, i) => (
                <div key={i} className="flex items-center gap-3 py-2 border-b border-dark-border/50 last:border-0">
                  <span className="text-gray-500 text-sm w-12">{event.time}'</span>
                  <div className="flex-1">
                    <p className="text-white text-sm">
                      {event.type === 'Goal' && '⚽ '}
                      {event.type === 'Card' && event.detail === 'Red Card' && '🟥 '}
                      {event.type === 'Card' && event.detail === 'Yellow Card' && '🟨 '}
                      {event.player}
                    </p>
                    {event.assist && (
                      <p className="text-gray-500 text-xs">Asistencia: {event.assist}</p>
                    )}
                  </div>
                  <span className="text-gray-500 text-xs">{event.team}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
