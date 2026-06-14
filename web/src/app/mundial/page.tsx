'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Globe, Trophy, Calendar, Swords, Loader2, Goal, ChevronRight, ArrowLeft } from 'lucide-react'
import { apiGet } from '@/lib/api'

interface GroupTeam {
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
}

interface Group {
  name: string
  teams: GroupTeam[]
}

interface Fixture {
  id: number
  date: string
  status: string
  elapsed: number | null
  round: string
  home: { id: number; name: string; logo: string }
  away: { id: number; name: string; logo: string }
  goals: { home: number | null; away: number | null }
}

interface Scorer {
  position: number
  team_code: string
  team_name: string
  goals: number
  matches: number
  avg: number
}

type Tab = 'grupos' | 'partidos' | 'goleadores'

export default function MundialPage() {
  const [tab, setTab] = useState<Tab>('grupos')
  const [groups, setGroups] = useState<Group[]>([])
  const [fixtures, setFixtures] = useState<Fixture[]>([])
  const [scorers, setScorers] = useState<Scorer[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      apiGet('/api/mundial/standings'),
      apiGet('/api/mundial/fixtures'),
      apiGet('/api/mundial/topscorers'),
    ]).then(([s, f, sc]) => {
      setGroups(s.groups || [])
      setFixtures(f.fixtures || [])
      setScorers(sc.scorers || [])
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-gradient-to-r from-blue-900/50 to-yellow-900/30 border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Globe className="w-6 h-6 text-yellow-400" />
          <h1 className="text-lg font-bold text-white">Mundial ⚽</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="flex gap-2 mb-6">
          {[
            { key: 'grupos' as Tab, icon: <Swords className="w-4 h-4" />, label: 'Grupos' },
            { key: 'partidos' as Tab, icon: <Calendar className="w-4 h-4" />, label: 'Partidos' },
            { key: 'goleadores' as Tab, icon: <Goal className="w-4 h-4" />, label: 'Goleadores' },
          ].map(t => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                tab === t.key
                  ? 'bg-yellow-500 text-black'
                  : 'bg-dark-card text-gray-400 hover:text-white border border-dark-border'
              }`}
            >
              {t.icon}
              {t.label}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-yellow-400 animate-spin" />
          </div>
        ) : tab === 'grupos' ? (
          <GroupsTab groups={groups} />
        ) : tab === 'partidos' ? (
          <FixturesTab fixtures={fixtures} />
        ) : (
          <ScorersTab scorers={scorers} />
        )}
      </main>
    </div>
  )
}

function GroupsTab({ groups }: { groups: Group[] }) {
  if (groups.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <Trophy className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No hay datos disponibles del Mundial</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {groups.map(group => (
        <div key={group.name} className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
          <div className="bg-yellow-500/10 px-4 py-2 border-b border-dark-border">
            <h3 className="font-bold text-yellow-400 text-sm">{group.name}</h3>
          </div>
          <table className="w-full text-xs">
            <thead>
              <tr className="text-gray-500 uppercase border-b border-dark-border/50">
                <th className="text-left px-3 py-2">#</th>
                <th className="text-left px-3 py-2">Equipo</th>
                <th className="text-center px-2 py-2">PJ</th>
                <th className="text-center px-2 py-2">DG</th>
                <th className="text-center px-3 py-2 font-bold">Pts</th>
              </tr>
            </thead>
            <tbody>
              {group.teams.map(team => {
                const bgClass = team.position <= 2 ? 'bg-green-500/5' : ''
                return (
                  <tr key={team.team_id} className={`${bgClass} border-b border-dark-border/30`}>
                    <td className="px-3 py-2 text-gray-400">{team.position}</td>
                    <td className="px-3 py-2">
                      <div className="flex items-center gap-2">
                        {team.team_logo && (team.team_logo.startsWith('http') ? <img src={team.team_logo} alt="" className="w-5 h-5" /> : <span className="text-lg">{team.team_logo}</span>)}
                        <span className="text-white font-medium">{team.team_name}</span>
                      </div>
                    </td>
                    <td className="text-center px-2 py-2 text-gray-400">{team.played}</td>
                    <td className={`text-center px-2 py-2 ${team.goal_difference > 0 ? 'text-green-400' : team.goal_difference < 0 ? 'text-red-400' : 'text-gray-400'}`}>
                      {team.goal_difference > 0 ? '+' : ''}{team.goal_difference}
                    </td>
                    <td className="text-center px-3 py-2 text-white font-bold">{team.points}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  )
}

function FixturesTab({ fixtures }: { fixtures: Fixture[] }) {
  if (fixtures.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No hay partidos cargados</p>
      </div>
    )
  }

  const live = fixtures.filter(f => f.status === 'LIVE')
  const finished = fixtures.filter(f => f.status === 'FT')
  const upcoming = fixtures.filter(f => f.status === 'SCHEDULED')

  const renderMatch = (f: Fixture, showDate: boolean) => {
    const date = new Date(f.date)
    const dateStr = date.toLocaleDateString('es-AR', { day: 'numeric', month: 'short' })
    const timeStr = date.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })
    const isLive = f.status === 'LIVE'
    return (
      <div key={f.id} className="bg-dark-card border border-dark-border rounded-xl p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <span className="text-white text-sm font-medium truncate">{f.home.name}</span>
          </div>
          <div className={`flex items-center gap-3 mx-4 ${isLive ? 'text-green-400' : ''}`}>
            {isLive && <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />}
            {finished.includes(f) ? (
              <>
                <span className="text-lg font-bold text-white">{f.goals.home ?? '-'}</span>
                <span className="text-gray-500 text-xs">vs</span>
                <span className="text-lg font-bold text-white">{f.goals.away ?? '-'}</span>
              </>
            ) : (
              <div className="text-center">
                <span className="text-yellow-400 text-xs font-bold">{showDate ? dateStr : ''}</span>
                <span className="block text-gray-500 text-xs">{showDate ? timeStr : f.round}</span>
              </div>
            )}
          </div>
          <div className="flex items-center gap-3 flex-1 min-w-0 justify-end">
            <span className="text-white text-sm font-medium truncate">{f.away.name}</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {live.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-green-400 uppercase mb-3">En vivo</h3>
          <div className="space-y-2">
            {live.map(f => renderMatch(f, true))}
          </div>
        </div>
      )}

      {finished.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-gray-500 uppercase mb-3">Resultados</h3>
          <div className="space-y-2">
            {finished.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).map(f => renderMatch(f, false))}
          </div>
        </div>
      )}

      {upcoming.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-gray-500 uppercase mb-3">Próximos</h3>
          <div className="space-y-2">
            {upcoming.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()).map(f => renderMatch(f, true))}
          </div>
        </div>
      )}
    </div>
  )
}

function ScorersTab({ scorers }: { scorers: Scorer[] }) {
  if (scorers.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <Goal className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No hay datos de goleadores</p>
        <p className="text-xs mt-2">Los datos individuales estarán disponibles cuando tengamos una API key de datos en vivo</p>
      </div>
    )
  }

  return (
    <div className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
      <div className="bg-yellow-500/10 px-4 py-2 border-b border-dark-border">
        <p className="text-xs text-gray-400">Goles por equipo (datos de partidos finalizados)</p>
      </div>
      <table className="w-full">
        <thead>
          <tr className="border-b border-dark-border text-gray-500 text-xs uppercase">
            <th className="text-left px-4 py-3">#</th>
            <th className="text-left px-4 py-3">Equipo</th>
            <th className="text-center px-4 py-3">PJ</th>
            <th className="text-center px-4 py-3">Goles</th>
            <th className="text-center px-4 py-3">Promedio</th>
          </tr>
        </thead>
        <tbody>
          {scorers.map(s => (
            <tr key={s.team_code} className="border-b border-dark-border/50">
              <td className="px-4 py-3 text-gray-400 text-sm">{s.position}</td>
              <td className="px-4 py-3">
                <span className="text-white text-sm font-medium">{s.team_name}</span>
              </td>
              <td className="px-4 py-3 text-center text-gray-400 text-sm">{s.matches}</td>
              <td className="px-4 py-3 text-center text-yellow-400 font-bold text-lg">{s.goals}</td>
              <td className="px-4 py-3 text-center text-gray-400 text-sm">{s.avg}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
