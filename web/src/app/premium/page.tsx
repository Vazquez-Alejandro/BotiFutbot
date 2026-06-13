'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Crown, ArrowLeft, Check, Zap, Star, Shield, X, Loader2, ExternalLink, TrendingUp } from 'lucide-react'
import { LIGAS } from '@/lib/ligas'

const PLANS = {
  free: {
    name: 'Gratuito',
    price: 0,
    period: 'siempre',
    color: 'text-gray-400',
    bg: 'bg-gray-500/20',
    border: 'border-gray-500/30',
    features: {
      equipos: '3 equipos',
      delay: '60 seg',
      ads: 'Anuncios',
      predicciones: '✗',
      stats: 'Básicas',
    },
  },
  premium: {
    name: 'Premium',
    price: 499,
    period: 'mes',
    color: 'text-primary',
    bg: 'bg-primary/20',
    border: 'border-primary/50',
    features: {
      equipos: '20 equipos',
      delay: 'Tiempo real',
      ads: 'Sin anuncios',
      predicciones: '✓',
      stats: 'Avanzadas',
    },
  },
  pro: {
    name: 'Pro',
    price: 999,
    period: 'mes',
    color: 'text-purple-400',
    bg: 'bg-purple-500/20',
    border: 'border-purple-500/50',
    features: {
      equipos: '50 equipos',
      delay: 'Tiempo real',
      ads: 'Sin anuncios',
      predicciones: '✓',
      stats: 'Avanzadas',
      api: 'API Access',
    },
  },
}

export default function PremiumPage() {
  const [selected, setSelected] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubscribe = async (plan: string) => {
    setSelected(plan)
    setLoading(true)
    await new Promise(r => setTimeout(r, 1000))
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Crown className="w-5 h-5 text-yellow-400" />
          <h1 className="text-lg font-bold text-white">Premium</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-white mb-3">
            Llevá tu experiencia al <span className="text-primary">siguiente nivel</span>
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            Sin anuncios, notificaciones en tiempo real, estadísticas avanzadas y mucho más.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {Object.entries(PLANS).map(([key, plan]) => (
            <div
              key={key}
              className={`relative bg-dark-card border rounded-2xl p-6 transition ${
                selected === key
                  ? `${plan.border} ring-2 ring-primary/20`
                  : 'border-dark-border hover:border-gray-600'
              }`}
            >
              {key === 'premium' && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-xs font-medium">
                  Más popular
                </div>
              )}

              <div className={`w-12 h-12 ${plan.bg} rounded-xl flex items-center justify-center mb-4`}>
                {key === 'free' ? <Star className={`w-6 h-6 ${plan.color}`} /> :
                 key === 'premium' ? <Zap className={`w-6 h-6 ${plan.color}`} /> :
                 <Crown className={`w-6 h-6 ${plan.color}`} />}
              </div>

              <h3 className={`text-xl font-bold text-white mb-1`}>{plan.name}</h3>
              <div className="mb-6">
                <span className="text-3xl font-bold text-white">${plan.price}</span>
                {plan.price > 0 && <span className="text-gray-500 text-sm ml-1">/{plan.period}</span>}
              </div>

              <div className="space-y-3 mb-8">
                {Object.entries(plan.features).map(([key, val]) => (
                  <div key={key} className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 capitalize">{key}</span>
                    <span className={
                      val === '✓' ? 'text-primary' :
                      val === '✗' ? 'text-red-400' :
                      val === 'Sin anuncios' ? 'text-primary' :
                      'text-white'
                    }>{val}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => handleSubscribe(key)}
                disabled={key === 'free' || loading}
                className={`w-full py-3 rounded-xl font-medium transition ${
                  key === 'free'
                    ? 'bg-dark border border-dark-border text-gray-500 cursor-default'
                    : selected === key
                    ? 'bg-primary text-white'
                    : 'bg-primary/10 text-primary hover:bg-primary/20'
                }`}
              >
                {selected === key && loading ? (
                  <Loader2 className="w-5 h-5 animate-spin mx-auto" />
                ) : key === 'free' ? (
                  'Plan actual'
                ) : (
                  'Suscribirse'
                )}
              </button>
            </div>
          ))}
        </div>

        <div className="bg-dark-card border border-dark-border rounded-2xl p-8">
          <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
            <TrendingUp className="w-5 h-5 text-primary" />
            Ganá con tus recomendaciones
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-dark border border-dark-border rounded-xl p-4 text-center">
              <p className="text-2xl font-bold text-primary">20%</p>
              <p className="text-gray-500 text-sm">Comisión Bet365</p>
            </div>
            <div className="bg-dark border border-dark-border rounded-xl p-4 text-center">
              <p className="text-2xl font-bold text-primary">25%</p>
              <p className="text-gray-500 text-sm">Comisión Betano</p>
            </div>
            <div className="bg-dark border border-dark-border rounded-xl p-4 text-center">
              <p className="text-2xl font-bold text-primary">15%</p>
              <p className="text-gray-500 text-sm">Comisión Sportingbet</p>
            </div>
          </div>

          <p className="text-gray-400 text-sm text-center">
            Compartí tus enlaces de afiliado y ganá comisiones por cada usuario que se registre.
            Los pagos se acreditan automáticamente a tu cuenta.
          </p>
        </div>
      </main>
    </div>
  )
}
