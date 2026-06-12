import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'BotifutBot - Fútbol en tiempo real',
  description: 'Noticias, estadísticas y competiciones de fútbol',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-dark">
        {children}
      </body>
    </html>
  )
}
