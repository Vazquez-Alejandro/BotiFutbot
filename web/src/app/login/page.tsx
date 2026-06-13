'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, LogIn, Loader2, AlertCircle } from 'lucide-react'

export default function LoginPage() {
  const [verifying, setVerifying] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get('token')
    if (token) {
      setVerifying(true)
      localStorage.setItem('botifutbol_token', token)
      window.location.href = '/dashboard'
    }
  }, [])

  return (
    <div className="min-h-screen bg-dark flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <Link href="/" className="inline-flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition">
          <ArrowLeft className="w-4 h-4" />
          Volver
        </Link>

        <div className="bg-dark-card border border-dark-border rounded-2xl p-8 text-center">
          <div className="w-20 h-20 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <LogIn className="w-10 h-10 text-primary" />
          </div>

          <h1 className="text-2xl font-bold text-white mb-2">Iniciar sesión</h1>
          <p className="text-gray-400 mb-8">
            Conectate con tu cuenta de Telegram para acceder a todas las funciones
          </p>

          {verifying ? (
            <div className="flex items-center justify-center gap-2 text-primary">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Verificando...</span>
            </div>
          ) : (
            <>
              <a
                href={`https://t.me/BotiFutBot?start=login`}
                className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-8 py-3 rounded-xl font-medium transition w-full justify-center"
              >
                <LogIn className="w-5 h-5" />
                Iniciar con Telegram
              </a>

              <p className="text-gray-500 text-xs mt-4">
                Al iniciar sesión aceptás nuestros términos y condiciones
              </p>
            </>
          )}

          {error && (
            <div className="mt-4 bg-red-500/10 border border-red-500/20 rounded-xl p-4 flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
