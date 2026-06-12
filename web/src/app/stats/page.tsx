'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { BarChart3, ArrowLeft, Loader2, Medal, Target, Users, Star } from 'lucide-react'
import { apiGet } from '@/lib/api'
import { LIGAS } from '@/lib/ligas'

interface Scorer {
  player_id: number
  name: string
  photo: string
  team: string
  team_logo: string
  goals: number
  assists: number | null
  appearances: number | null
  rating: string | null
}

export default function StatsPage() {
  const [selectedLiga, setSelectedLiga] = useState(LIGAS[0].id)
  const [scorers, setScorers] = useState<Scorer[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    apiGet(`/api/leagues/topscorers?league_id=${selectedLiga}&season=2024`)
      .then(data => setScorers(data.scorers || []))
      .catch(() => setScorers([]))
      .finally(() => setLoading(false))
  }, [selectedLiga])

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <BarChart3 className="w-5 h-5 text-primary" />
          <h1 className="text-lg font-bold text-white">Estadísticas</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide">
          {LIGAS.map(liga => (
            <button
              key={liga.id}
              onClick={() => setSelectedLiga(liga.id)}
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

        <div className="mb-6">
          <h2 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
            <Medal className="w-5 h-5 text-yellow-400" />
            Goleadores
          </h2>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
          </div>
        ) : scorers.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No hay estadísticas disponibles
          </div>
        ) : (
          <div className="space-y-2">
            {scorers.map((s, i) => (
              <div key={s.player_id} className="bg-dark-card border border-dark-border rounded-xl p-4 flex items-center gap-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                  i === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                  i === 1 ? 'bg-gray-400/20 text-gray-300' :
                  i === 2 ? 'bg-orange-500/20 text-orange-400' :
                  'bg-dark text-gray-500'
                }`}>
                  {i + 1}
                </div>

                <img src={s.photo} alt="" className="w-10 h-10 rounded-full" />

                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium text-sm truncate">{s.name}</p>
                  <div className="flex items-center gap-2">
                    {s.team_logo && <img src={s.team_logo} alt="" className="w-4 h-4" />}
                    <p className="text-gray-500 text-xs truncate">{s.team}</p>
                  </div>
                </div>

                <div className="text-right">
                  <p className="text-primary font-bold text-lg">{s.goles}</p>
                  <p className="text-gray-500 text-xs">goles</p>
                </div>

                {s.assists && s.assists > 0 && (
                  <div className="text-right">
                    <p className="text-white font-medium">{s.assists}</p>
                    <p className="text-gray-500 text-xs">asist.</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
