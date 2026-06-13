'use client'

import Link from 'next/link'
import { Trophy, Calendar, Users, BarChart3, Zap, Radio, Crown, Globe, ChevronRight, ExternalLink, TrendingUp } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/logo.png" alt="BotiFutbol" className="w-10 h-10 rounded-xl" />
            <h1 className="text-xl font-bold text-white">BotiFutbol</h1>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/login" className="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-lg font-medium text-sm transition">
              Iniciar sesión
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <section className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">
            Tu fútbol, <span className="text-primary">tu app</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Seguí tus equipos, recibí notificaciones en tiempo real y competí con amigos.
            Bot de Telegram + App web.
          </p>

          <div className="flex items-center justify-center gap-3 mt-6">
            <a
              href="https://t.me/BotiFutBot"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-medium transition"
            >
              <Zap className="w-5 h-5" />
              Probar en Telegram
            </a>
            <Link
              href="/live"
              className="inline-flex items-center gap-2 bg-dark-card border border-dark-border hover:border-red-500/50 text-white px-6 py-3 rounded-xl font-medium transition"
            >
              <Radio className="w-5 h-5 text-red-400" />
              En Vivo
            </Link>
          </div>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <Link href="/mundial" className="md:col-span-2">
            <div className="bg-gradient-to-r from-blue-900/40 via-yellow-900/20 to-blue-900/40 border border-yellow-500/30 rounded-xl p-5 hover:border-yellow-400/50 transition cursor-pointer group">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Globe className="w-6 h-6 text-yellow-400" />
                  <div>
                    <h3 className="font-bold text-white">Mundial 2026</h3>
                    <p className="text-gray-400 text-sm">Grupos, resultados, fixture y goleadores</p>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-yellow-400/50 group-hover:text-yellow-400 transition" />
              </div>
            </div>
          </Link>
          <FeatureCard
            icon={<Radio className="w-6 h-6 text-red-400" />}
            title="En Vivo"
            description="Partidos en vivo con actualización cada 30 segundos"
            href="/live"
          />
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
          <FeatureCard
            icon={<Crown className="w-6 h-6 text-yellow-400" />}
            title="Premium"
            description="Sin anuncios, tiempo real, estadísticas avanzadas"
            href="/premium"
          />
        </div>

        <a
          href="https://www.betano.com"
          target="_blank"
          rel="noopener noreferrer"
          className="block bg-gradient-to-r from-yellow-600/20 to-yellow-800/20 border border-yellow-500/20 rounded-2xl p-6 mb-8 hover:opacity-90 transition text-center"
        >
          <p className="text-yellow-400 text-lg font-bold mb-1">🔥 ¡Apostá con Betano!</p>
          <p className="text-gray-400 text-sm">Cuotas en vivo, los mejores bonus y promociones exclusivas</p>
        </a>

        <section className="bg-dark-card rounded-2xl border border-dark-border p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-6 h-6 text-primary" />
            <h3 className="text-xl font-bold text-white">Ganá con tus recomendaciones</h3>
          </div>
          <p className="text-gray-400 mb-6">
            Compartí BotiFutbol con tus amigos y ganá hasta 25% de comisión por cada registro en las casas de apuestas.
            Tu enlace único de afiliado ya está activo en el bot.
          </p>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-dark border border-dark-border rounded-xl p-4">
              <p className="text-2xl font-bold text-primary">20%</p>
              <p className="text-gray-500 text-xs">Bet365</p>
            </div>
            <div className="bg-dark border border-dark-border rounded-xl p-4">
              <p className="text-2xl font-bold text-primary">25%</p>
              <p className="text-gray-500 text-xs">Betano</p>
            </div>
            <div className="bg-dark border border-dark-border rounded-xl p-4">
              <p className="text-2xl font-bold text-primary">15%</p>
              <p className="text-gray-500 text-xs">Sportingbet</p>
            </div>
          </div>
        </section>

        <section className="bg-dark-card rounded-2xl border border-dark-border p-8">
          <div className="flex items-center gap-3 mb-6">
            <Zap className="w-6 h-6 text-primary" />
            <h3 className="text-xl font-bold text-white">¿Cómo funciona?</h3>
          </div>
          <div className="space-y-4">
            <Step number={1} text="Conectá tu cuenta de Telegram con /start" />
            <Step number={2} text="Elegí tus equipos favoritos navegando por continentes" />
            <Step number={3} text="Recibí goles, tarjetos y resultados en tiempo real" />
            <Step number={4} text="Usá la web para ver clasificación, fixture y estadísticas" />
            <Step number={5} text="Competí con amigos y ganá con el programa de afiliados" />
          </div>
        </section>
      </main>

      <footer className="border-t border-dark-border mt-12 py-6 text-center text-gray-500 text-sm">
        <p>BotiFutbol © 2026 — ⚽ Hecho para los amantes del fútbol</p>
        <div className="flex items-center justify-center gap-4 mt-2">
          <Link href="/premium" className="hover:text-primary transition">Premium</Link>
          <Link href="/live" className="hover:text-primary transition">En Vivo</Link>
          <span>•</span>
          <span>Bot: @BotiFutBot</span>
        </div>
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
      <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
        {number}
      </div>
      <p className="text-gray-300">{text}</p>
    </div>
  )
}
