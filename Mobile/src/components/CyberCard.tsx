import { ReactNode } from 'react'

interface CyberCardProps {
  children: ReactNode
  className?: string
  glowOnHover?: boolean
}

export default function CyberCard({ children, className = '', glowOnHover = true }: CyberCardProps) {
  return (
    <div className={`glass-card p-6 ${glowOnHover ? 'hover-glow hover:border-neon-orange/50' : ''} ${className}`}>
      {children}
    </div>
  )
}
