'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Radio, ArrowLeft, Loader2 } from 'lucide-react'
import { useLiveMatches } from '@/lib/utils'

export default function LivePage() {
  const { matches, loading } = useLiveMatches()

  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Radio className="w-5 h-5 text-red-400" />
          <h1 className="text-lg font-bold text-white">En Vivo</h1>
          {matches.length > 0 && (
            <span className="bg-red-500/20 text-red-400 px-3 py-0.5 rounded-full text-xs font-medium animate-pulse">
              {matches.length} partidos
            </span>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-red-400 animate-spin" />
          </div>
        ) : matches.length === 0 ? (
          <div className="text-center py-12">
            <Radio className="w-16 h-16 text-gray-700 mx-auto mb-4" />
            <p className="text-gray-500">No hay partidos en vivo ahora</p>
            <p className="text-gray-600 text-sm mt-1">Volvé más tarde para ver la acción ⚽</p>
          </div>
        ) : (
          <div className="space-y-3">
            {matches.map((m: any) => (
              <Link key={m.id} href={`/match/${m.id}`}>
                <div className="bg-dark-card border border-dark-border rounded-xl p-4 hover:border-red-500/50 transition cursor-pointer">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                    <span className="text-red-400 text-xs font-medium">
                      EN VIVO {m.elapsed && `${m.elapsed}'`}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      {m.home.logo && <img src={m.home.logo} alt="" className="w-8 h-8" />}
                      <span className="text-white text-sm font-medium">{m.home.name}</span>
                    </div>

                    <div className="flex items-center gap-3 px-4">
                      <span className="text-2xl font-bold text-red-400">{m.goals.home ?? '-'}</span>
                      <span className="text-gray-600">-</span>
                      <span className="text-2xl font-bold text-red-400">{m.goals.away ?? '-'}</span>
                    </div>

                    <div className="flex items-center gap-3 flex-1 justify-end">
                      <span className="text-white text-sm font-medium">{m.away.name}</span>
                      {m.away.logo && <img src={m.away.logo} alt="" className="w-8 h-8" />}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        <div className="mt-8 bg-gradient-to-r from-green-600/10 to-green-800/10 border border-green-500/20 rounded-2xl p-6 text-center">
          <p className="text-green-400 text-lg font-bold mb-1">🎲 ¿Querés apostar?</p>
          <p className="text-gray-400 text-sm mb-4">
            Seguí las cuotas en vivo de todos los partidos con Bet365
          </p>
          <a
            href="https://www.bet365.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-xl font-medium transition"
          >
            Ver cuotas en Bet365 →
          </a>
        </div>
      </main>
    </div>
  )
}
