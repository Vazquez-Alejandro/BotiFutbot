'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Trophy, ArrowLeft, Loader2 } from 'lucide-react'
import { apiGet } from '@/lib/api'
import { LIGAS } from '@/lib/ligas'

interface Standing {
  position: number
  team_id: number
  team_name: string
  team_logo: string
  points: number
  played: number
  win: number
  draw: number
  lose: number
  goals_for: number
  goals_against: number
  goal_difference: number
  form: string
}

export default function StandingsPage() {
  const [selectedLiga, setSelectedLiga] = useState(LIGAS[0].id)
  const [standings, setStandings] = useState<Standing[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    apiGet(`/api/leagues/standings?league_id=${selectedLiga}&season=2024`)
      .then(data => setStandings(data.standings || []))
      .catch(() => setStandings([]))
      .finally(() => setLoading(false))
  }, [selectedLiga])

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Trophy className="w-5 h-5 text-primary" />
          <h1 className="text-lg font-bold text-white">Clasificación</h1>
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

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
          </div>
        ) : standings.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No hay datos de clasificación disponibles
          </div>
        ) : (
          <div className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dark-border text-gray-500 text-xs uppercase">
                  <th className="text-left px-4 py-3">#</th>
                  <th className="text-left px-4 py-3">Equipo</th>
                  <th className="text-center px-2 py-3">PJ</th>
                  <th className="text-center px-2 py-3">G</th>
                  <th className="text-center px-2 py-3">E</th>
                  <th className="text-center px-2 py-3">P</th>
                  <th className="text-center px-2 py-3">DG</th>
                  <th className="text-center px-4 py-3 font-bold text-white">Pts</th>
                </tr>
              </thead>
              <tbody>
                {standings.map((s) => (
                  <tr key={s.team_id} className="border-b border-dark-border/50 hover:bg-white/5 transition">
                    <td className="px-4 py-3 text-gray-400 text-sm">{s.position}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        {s.team_logo && (
                          <img src={s.team_logo} alt="" className="w-6 h-6" />
                        )}
                        <span className="text-white text-sm font-medium">{s.team_name}</span>
                      </div>
                    </td>
                    <td className="text-center px-2 py-3 text-gray-400 text-sm">{s.played}</td>
                    <td className="text-center px-2 py-3 text-green-400 text-sm">{s.win}</td>
                    <td className="text-center px-2 py-3 text-yellow-400 text-sm">{s.draw}</td>
                    <td className="text-center px-2 py-3 text-red-400 text-sm">{s.lose}</td>
                    <td className="text-center px-2 py-3 text-gray-400 text-sm">
                      {s.goal_difference > 0 ? '+' : ''}{s.goal_difference}
                    </td>
                    <td className="text-center px-4 py-3 text-white font-bold">{s.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}
