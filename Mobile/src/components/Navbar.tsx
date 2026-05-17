import { useState } from 'react'
import { Menu, X, Brain, Zap, Settings, User } from 'lucide-react'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-card border-b border-cyber-border/50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <Brain className="w-8 h-8 text-neon-red animate-pulse" />
            <span className="text-xl font-bold neon-text">SENTIENCE</span>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-300 hover:text-neon-orange transition-colors">
              Features
            </a>
            <a href="#stats" className="text-gray-300 hover:text-neon-orange transition-colors">
              Stats
            </a>
            <a href="#docs" className="text-gray-300 hover:text-neon-orange transition-colors">
              Docs
            </a>
            <button className="cyber-button text-sm">
              <Zap className="w-4 h-4 mr-2" />
              Get Started
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-white hover:text-neon-orange transition-colors"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-4 border-t border-cyber-border/50">
            <a href="#features" className="block text-gray-300 hover:text-neon-orange transition-colors">
              Features
            </a>
            <a href="#stats" className="block text-gray-300 hover:text-neon-orange transition-colors">
              Stats
            </a>
            <a href="#docs" className="block text-gray-300 hover:text-neon-orange transition-colors">
              Docs
            </a>
            <button className="cyber-button text-sm w-full">
              <Zap className="w-4 h-4 mr-2" />
              Get Started
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}
