import { Brain, Github, Twitter, Linkedin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="relative z-10 glass-card border-t border-cyber-border/50 mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Brain className="w-8 h-8 text-neon-red animate-pulse" />
              <span className="text-xl font-bold neon-text">SENTIENCE</span>
            </div>
            <p className="text-gray-400 text-sm">
              Next-generation cognitive operating system powered by advanced AI
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="text-white font-semibold mb-4 uppercase tracking-wider">Product</h3>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="#" className="hover:text-neon-orange transition-colors">Features</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">API Reference</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-white font-semibold mb-4 uppercase tracking-wider">Company</h3>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="#" className="hover:text-neon-orange transition-colors">About</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-neon-orange transition-colors">Contact</a></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="text-white font-semibold mb-4 uppercase tracking-wider">Connect</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-neon-orange transition-colors">
                <Github className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-neon-orange transition-colors">
                <Twitter className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-neon-orange transition-colors">
                <Linkedin className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-cyber-border/50 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; 2026 Sentience Layer. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
