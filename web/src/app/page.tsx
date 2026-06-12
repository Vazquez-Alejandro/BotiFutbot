'use client'

import Link from 'next/link'
import { Trophy, Calendar, Users, BarChart3, Zap, ChevronRight } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/logo.png" alt="BotifutBot" className="w-10 h-10 rounded-xl" />
            <h1 className="text-xl font-bold text-white">BotifutBot</h1>
          </div>
          <Link href="/login" className="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-lg font-medium transition">
            Iniciar sesión
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <section className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">
            Tu fútbol, <span className="text-primary">tuapp</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Seguí tus equipos favoritos, competí con amigos y enterate de todo en tiempo real.
          </p>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
          <FeatureCard
            icon={<Trophy className="w-6 h-6 text-primary" />}
            title="Clasificación"
            description="Tablas de posiciones actualizadas de todas las ligas"
            href="/standings"
          />
          <FeatureCard
            icon={<Calendar className="w-6 h-6 text-primary" />}
            title="Fixture"
            description="Calendario completo de partidos con fechas y horarios"
            href="/fixture"
          />
          <FeatureCard
            icon={<Users className="w-6 h-6 text-primary" />}
            title="Amigos"
            description="Competí con tus amigos y hacé predicciones"
            href="/friends"
          />
          <FeatureCard
            icon={<BarChart3 className="w-6 h-6 text-primary" />}
            title="Estadísticas"
            description="Goleadores, asistencias y rendimiento de jugadores"
            href="/stats"
          />
        </div>

        <section className="bg-dark-card rounded-2xl border border-dark-border p-8">
          <div className="flex items-center gap-3 mb-6">
            <Zap className="w-6 h-6 text-primary" />
            <h3 className="text-xl font-bold text-white">¿Cómo funciona?</h3>
          </div>
          <div className="space-y-4">
            <Step number={1} text="Conectá tu cuenta de Telegram" />
            <Step number={2} text="Elegí tus equipos favoritos" />
            <Step number={3} text="Recibí notificaciones en tiempo real" />
            <Step number={4} text="Competí con amigos en predicciones" />
          </div>
        </section>
      </main>

      <footer className="border-t border-dark-border mt-12 py-6 text-center text-gray-500 text-sm">
        <p>BotifutBot © 2026 — Hecho con ⚽ para los amantes del fútbol</p>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description, href }: {
  icon: React.ReactNode
  title: string
  description: string
  href: string
}) {
  return (
    <Link href={href}>
      <div className="bg-dark-card border border-dark-border rounded-xl p-6 hover:border-primary/50 transition cursor-pointer group">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {icon}
            <h3 className="font-semibold text-white">{title}</h3>
          </div>
          <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-primary transition" />
        </div>
        <p className="text-gray-400 mt-2 text-sm">{description}</p>
      </div>
    </Link>
  )
}

function Step({ number, text }: { number: number; text: string }) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold text-sm">
        {number}
      </div>
      <p className="text-gray-300">{text}</p>
    </div>
  )
}
