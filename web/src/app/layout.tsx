import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'BotiFutbol - Fútbol en tiempo real',
  description: 'Noticias, estadísticas, partidos en vivo y competiciones de fútbol',
  icons: { icon: '/logo.png' },
  openGraph: {
    title: 'BotiFutbol - Fútbol en tiempo real',
    description: 'Seguí tus equipos, recibí notificaciones y competí con amigos',
    images: ['/logo.png'],
  },
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
