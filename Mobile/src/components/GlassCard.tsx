import { ReactNode } from 'react'

interface GlassCardProps {
  icon: ReactNode
  title: string
  description: string
  glowColor?: 'red' | 'orange' | 'amber'
}

export default function GlassCard({ icon, title, description, glowColor = 'red' }: GlassCardProps) {
  const glowClasses = {
    red: 'hover:shadow-neon hover:border-neon-red/50',
    orange: 'hover:shadow-neon-orange hover:border-neon-orange/50',
    amber: 'hover:shadow-neon-amber hover:border-neon-amber/50',
  }

  return (
    <div className={`glass-card p-6 hover-glow group cursor-pointer ${glowClasses[glowColor]}`}>
      <div className="mb-4 transform group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>

      <h3 className="text-xl font-bold mb-3 text-white group-hover:text-glow transition-all">
        {title}
      </h3>

      <p className="text-gray-400 leading-relaxed">
        {description}
      </p>

      <div className="mt-4 h-1 w-0 group-hover:w-full bg-gradient-to-r from-neon-red via-neon-orange to-neon-amber transition-all duration-500 rounded-full" />
    </div>
  )
}
