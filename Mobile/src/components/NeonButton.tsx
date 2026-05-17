import { ReactNode } from 'react'

interface NeonButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary'
  size?: 'md' | 'lg'
  onClick?: () => void
}

export default function NeonButton({
  children,
  variant = 'primary',
  size = 'md',
  onClick
}: NeonButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center font-semibold uppercase tracking-wider rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-glow'

  const variantClasses = {
    primary: 'bg-gradient-to-r from-neon-red to-neon-orange border border-neon-orange/50 text-white',
    secondary: 'glass-card border-neon-red/30 text-white hover:border-neon-orange/50',
  }

  const sizeClasses = {
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base',
  }

  return (
    <button
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
    >
      {children}
    </button>
  )
}
