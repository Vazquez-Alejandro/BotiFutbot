'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Home, Trophy, Calendar, Users, BarChart3, Crown, ChevronRight, LogOut, Zap } from 'lucide-react'

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const saved = localStorage.getItem('botifutbol_user')
    if (saved) setUser(JSON.parse(saved))
  }, [])

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/logo.png" alt="BotifutBot" className="w-10 h-10 rounded-xl" />
            <div>
              <h1 className="text-lg font-bold text-white">BotifutBot</h1>
              {user && (
                <p className="text-xs text-gray-500">@{user.username || user.first_name}</p>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Link href="/premium" className="flex items-center gap-1 bg-yellow-500/10 text-yellow-400 px-3 py-1.5 rounded-lg text-xs font-medium hover:bg-yellow-500/20 transition">
              <Crown className="w-3.5 h-3.5" />
              Premium
            </Link>
            <button className="text-gray-500 hover:text-white transition">
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        {user && (
          <div className="bg-dark-card border border-dark-border rounded-2xl p-6 mb-6 flex items-center gap-4">
            {user.photo_url ? (
              <img src={user.photo_url} alt="" className="w-16 h-16 rounded-full" />
            ) : (
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-2xl text-primary font-bold">
                  {user.first_name?.charAt(0)}
                </span>
              </div>
            )}
            <div>
              <h2 className="text-xl font-bold text-white">{user.first_name}</h2>
              <p className="text-gray-500">@{user.username || 'sin username'}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <StatCard icon={<Trophy className="w-5 h-5" />} label="Equipos" value="3" color="text-primary" />
          <StatCard icon={<Crown className="w-5 h-5" />} label="Plan" value="Gratuito" color="text-yellow-400" />
          <StatCard icon={<Zap className="w-5 h-5" />} label="Predicciones" value="12" color="text-purple-400" />
          <StatCard icon={<BarChart3 className="w-5 h-5" />} label="Puntos" value="45" color="text-green-400" />
        </div>

        <div className="space-y-3">
          <NavCard
            icon={<Trophy className="w-5 h-5 text-primary" />}
            title="Clasificación"
            desc="Tablas de posiciones"
            href="/standings"
          />
          <NavCard
            icon={<Calendar className="w-5 h-5 text-primary" />}
            title="Fixture"
            desc="Calendario de partidos"
            href="/fixture"
          />
          <NavCard
            icon={<Users className="w-5 h-5 text-primary" />}
            title="Amigos"
            desc="Competí y hacé predicciones"
            href="/friends"
          />
          <NavCard
            icon={<BarChart3 className="w-5 h-5 text-primary" />}
            title="Estadísticas"
            desc="Goleadores y rendimiento"
            href="/stats"
          />
          <NavCard
            icon={<Crown className="w-5 h-5 text-yellow-400" />}
            title="Premium"
            desc="Sin anuncios, tiempo real, más features"
            href="/premium"
          />
        </div>
      </main>
    </div>
  )
}

function StatCard({ icon, label, value, color }: {
  icon: React.ReactNode
  label: string
  value: string
  color: string
}) {
  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-4 text-center">
      <div className={`mb-2 flex justify-center ${color}`}>{icon}</div>
      <p className={`text-lg font-bold ${color}`}>{value}</p>
      <p className="text-gray-500 text-xs">{label}</p>
    </div>
  )
}

function NavCard({ icon, title, desc, href }: {
  icon: React.ReactNode
  title: string
  desc: string
  href: string
}) {
  return (
    <Link href={href}>
      <div className="bg-dark-card border border-dark-border rounded-xl p-4 flex items-center justify-between hover:border-primary/50 transition cursor-pointer group">
        <div className="flex items-center gap-3">
          {icon}
          <div>
            <p className="text-white font-medium">{title}</p>
            <p className="text-gray-500 text-xs">{desc}</p>
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-primary transition" />
      </div>
    </Link>
  )
}
