'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Calendar, ArrowLeft, Loader2, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiGet } from '@/lib/api'
import { LIGAS } from '@/lib/ligas'

interface Match {
  id: number
  date: string
  status: string
  status_long: string
  elapsed: number | null
  round: string
  home: { id: number; name: string; logo: string; winner: boolean | null }
  away: { id: number; name: string; logo: string; winner: boolean | null }
  goals: { home: number | null; away: number | null }
}

export default function FixturePage() {
  const [selectedLiga, setSelectedLiga] = useState(LIGAS[0].id)
  const [fixtures, setFixtures] = useState<Match[]>([])
  const [loading, setLoading] = useState(true)
  const [currentRound, setCurrentRound] = useState(1)

  useEffect(() => {
    setLoading(true)
    apiGet(`/api/leagues/fixtures?league_id=${selectedLiga}&season=2024`)
      .then(data => setFixtures(data.fixtures || []))
      .catch(() => setFixtures([]))
      .finally(() => setLoading(false))
  }, [selectedLiga])

  const rounds = [...new Set(fixtures.map(f => f.round))].sort()
  const currentRoundName = rounds[currentRound - 1] || rounds[0]
  const roundFixtures = fixtures.filter(f => f.round === currentRoundName)

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Calendar className="w-5 h-5 text-primary" />
          <h1 className="text-lg font-bold text-white">Fixture</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide">
          {LIGAS.map(liga => (
            <button
              key={liga.id}
              onClick={() => { setSelectedLiga(liga.id); setCurrentRound(1) }}
              className={`flex-shrink-0 px-4 py-2 rounded-lg text-sm font-medium transition ${
                selectedLiga === liga.id
                  ? 'bg-primary text-white'
                  : 'bg-dark-card text-gray-400 hover:text-white border border-dark-border'
              }`}
            >
              {liga.pais}
            </button>
          ))}
        </div>

        {rounds.length > 0 && (
          <div className="flex items-center justify-between mb-6 bg-dark-card rounded-xl border border-dark-border p-4">
            <button
              onClick={() => setCurrentRound(Math.max(1, currentRound - 1))}
              disabled={currentRound <= 1}
              className="text-gray-400 hover:text-white disabled:opacity-30"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            <div className="text-center">
              <p className="text-white font-semibold">{currentRoundName}</p>
              <p className="text-gray-500 text-xs">Jornada {currentRound} de {rounds.length}</p>
            </div>
            <button
              onClick={() => setCurrentRound(Math.min(rounds.length, currentRound + 1))}
              disabled={currentRound >= rounds.length}
              className="text-gray-400 hover:text-white disabled:opacity-30"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
          </div>
        ) : roundFixtures.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No hay partidos para esta jornada
          </div>
        ) : (
          <div className="space-y-3">
            {roundFixtures.map(match => (
              <MatchCard key={match.id} match={match} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

function MatchCard({ match }: { match: Match }) {
  const isLive = ['1H', '2H', 'HT', 'ET', 'P', 'LIVE'].includes(match.status)
  const isFinished = match.status === 'FT'

  return (
    <Link href={`/match/${match.id}`}>
      <div className="bg-dark-card border border-dark-border rounded-xl p-4 hover:border-primary/50 transition cursor-pointer">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
          <span>{new Date(match.date).toLocaleDateString('es-AR', { weekday: 'short', day: 'numeric', month: 'short' })}</span>
          <span>{new Date(match.date).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}</span>
          {isLive && (
            <span className="bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full text-xs font-medium animate-pulse">
              EN VIVO {match.elapsed && `${match.elapsed}'`}
            </span>
          )}
          {isFinished && (
            <span className="text-gray-500 text-xs">FINAL</span>
          )}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 flex-1">
            {match.home.logo && <img src={match.home.logo} alt="" className="w-8 h-8" />}
            <span className={`text-sm font-medium ${match.home.winner ? 'text-white' : 'text-gray-400'}`}>
              {match.home.name}
            </span>
          </div>

          <div className="flex items-center gap-2 px-4">
            <span className={`text-lg font-bold ${isLive ? 'text-primary' : 'text-white'}`}>
              {match.goals.home ?? '-'}
            </span>
            <span className="text-gray-600">-</span>
            <span className={`text-lg font-bold ${isLive ? 'text-primary' : 'text-white'}`}>
              {match.goals.away ?? '-'}
            </span>
          </div>

          <div className="flex items-center gap-3 flex-1 justify-end">
            <span className={`text-sm font-medium text-right ${match.away.winner ? 'text-white' : 'text-gray-400'}`}>
              {match.away.name}
            </span>
            {match.away.logo && <img src={match.away.logo} alt="" className="w-8 h-8" />}
          </div>
        </div>
      </div>
    </Link>
  )
}
