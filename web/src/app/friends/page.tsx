'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Users, ArrowLeft, UserPlus, Trophy, Target, Star } from 'lucide-react'

export default function FriendsPage() {
  return (
    <div className="min-h-screen bg-dark">
      <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Users className="w-5 h-5 text-primary" />
          <h1 className="text-lg font-bold text-white">Amigos</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-dark-card border border-dark-border rounded-2xl p-8 text-center mb-8">
          <UserPlus className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Conectate con amigos</h2>
          <p className="text-gray-400 mb-6">
            Agregá amigos para competir con predicciones y ver quién acierta más goles.
          </p>
          <button className="bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-medium transition">
            Buscar amigos
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-dark-card border border-dark-border rounded-xl p-6 text-center">
            <Trophy className="w-8 h-8 text-yellow-400 mx-auto mb-3" />
            <h3 className="text-white font-semibold mb-1">Competencia</h3>
            <p className="text-gray-500 text-sm">Hacé predicciones y competí por el podio</p>
          </div>

          <div className="bg-dark-card border border-dark-border rounded-xl p-6 text-center">
            <Target className="w-8 h-8 text-primary mx-auto mb-3" />
            <h3 className="text-white font-semibold mb-1">Predicciones</h3>
            <p className="text-gray-500 text-sm">Adiviná los resultados y ganá puntos</p>
          </div>

          <div className="bg-dark-card border border-dark-border rounded-xl p-6 text-center">
            <Star className="w-8 h-8 text-purple-400 mx-auto mb-3" />
            <h3 className="text-white font-semibold mb-1">Ranking</h3>
            <p className="text-gray-500 text-sm">Vos contra tus amigos en tiempo real</p>
          </div>
        </div>
      </main>
    </div>
  )
}
