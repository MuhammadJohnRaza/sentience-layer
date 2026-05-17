import { useState } from 'react'
import { Send, Sparkles } from 'lucide-react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import CyberCard from '@/components/CyberCard'
import CyberInput from '@/components/CyberInput'
import NeonButton from '@/components/NeonButton'
import FloatingParticles from '@/components/FloatingParticles'

export default function Dashboard() {
  const [message, setMessage] = useState('')

  return (
    <div className="min-h-screen relative overflow-hidden">
      <FloatingParticles />
      <Navbar />

      <main className="relative z-10 container mx-auto px-4 pt-24 pb-12">
        <div className="space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold neon-text text-glow">
              AI Dashboard
            </h1>
            <p className="text-gray-400 text-lg">
              Monitor and control your cognitive systems
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <CyberCard>
              <div className="space-y-2">
                <div className="text-sm text-gray-400 uppercase tracking-wider">Active Agents</div>
                <div className="text-4xl font-bold neon-text">127</div>
                <div className="text-xs text-green-400">↑ 12% from last hour</div>
              </div>
            </CyberCard>

            <CyberCard>
              <div className="space-y-2">
                <div className="text-sm text-gray-400 uppercase tracking-wider">Processing Speed</div>
                <div className="text-4xl font-bold neon-text">2.4ms</div>
                <div className="text-xs text-green-400">↓ 8% latency reduction</div>
              </div>
            </CyberCard>

            <CyberCard>
              <div className="space-y-2">
                <div className="text-sm text-gray-400 uppercase tracking-wider">Success Rate</div>
                <div className="text-4xl font-bold neon-text">99.8%</div>
                <div className="text-xs text-green-400">↑ 0.3% improvement</div>
              </div>
            </CyberCard>
          </div>

          {/* Chat Interface */}
          <CyberCard className="min-h-[400px] flex flex-col">
            <div className="flex items-center space-x-2 mb-4 pb-4 border-b border-cyber-border/50">
              <Sparkles className="w-5 h-5 text-neon-orange" />
              <h2 className="text-xl font-semibold text-white">AI Assistant</h2>
            </div>

            <div className="flex-1 space-y-4 mb-4">
              <div className="glass-card p-4 max-w-[80%]">
                <p className="text-gray-300">Hello! How can I assist you today?</p>
              </div>
            </div>

            <div className="flex gap-2">
              <CyberInput
                placeholder="Type your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="flex-1"
              />
              <NeonButton variant="primary">
                <Send className="w-5 h-5" />
              </NeonButton>
            </div>
          </CyberCard>

          {/* Activity Feed */}
          <CyberCard>
            <h2 className="text-xl font-semibold text-white mb-4">Recent Activity</h2>
            <div className="space-y-3">
              {[
                { action: 'Neural network trained', time: '2 minutes ago', status: 'success' },
                { action: 'Data pipeline executed', time: '5 minutes ago', status: 'success' },
                { action: 'Model deployed to production', time: '12 minutes ago', status: 'success' },
                { action: 'System health check completed', time: '18 minutes ago', status: 'success' },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 glass-card">
                  <div>
                    <div className="text-white">{item.action}</div>
                    <div className="text-xs text-gray-400">{item.time}</div>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                </div>
              ))}
            </div>
          </CyberCard>
        </div>
      </main>

      <Footer />
    </div>
  )
}
