import { Brain, Zap, Cpu, Network, Sparkles, Flame } from 'lucide-react'
import GlassCard from '@/components/GlassCard'
import NeonButton from '@/components/NeonButton'
import FloatingParticles from '@/components/FloatingParticles'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden">
      <FloatingParticles />
      <Navbar />

      {/* Hero Section */}
      <section className="relative z-10 container mx-auto px-4 pt-24 pb-20">
        <div className="text-center space-y-8">
          <div className="inline-block">
            <Flame className="w-20 h-20 text-neon-orange animate-pulse mx-auto mb-4" />
          </div>

          <h1 className="text-6xl md:text-8xl font-bold neon-text text-glow animate-float">
            SENTIENCE LAYER
          </h1>

          <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto">
            Next-Generation Cognitive Operating System
          </p>

          <div className="flex gap-4 justify-center flex-wrap">
            <NeonButton variant="primary">
              <Zap className="w-5 h-5 mr-2" />
              Launch System
            </NeonButton>
            <NeonButton variant="secondary">
              <Brain className="w-5 h-5 mr-2" />
              Explore AI
            </NeonButton>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative z-10 container mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <GlassCard
            icon={<Brain className="w-8 h-8 text-neon-red" />}
            title="Neural Networks"
            description="Advanced AI-powered cognitive processing with real-time learning capabilities"
            glowColor="red"
          />

          <GlassCard
            icon={<Cpu className="w-8 h-8 text-neon-orange" />}
            title="Quantum Processing"
            description="Leverage quantum computing for unprecedented computational power"
            glowColor="orange"
          />

          <GlassCard
            icon={<Network className="w-8 h-8 text-neon-amber" />}
            title="Distributed Intelligence"
            description="Seamlessly connect and orchestrate multiple AI agents across networks"
            glowColor="amber"
          />

          <GlassCard
            icon={<Sparkles className="w-8 h-8 text-neon-red" />}
            title="Adaptive Learning"
            description="Self-improving algorithms that evolve with your data patterns"
            glowColor="red"
          />

          <GlassCard
            icon={<Zap className="w-8 h-8 text-neon-orange" />}
            title="Real-time Processing"
            description="Lightning-fast inference with sub-millisecond response times"
            glowColor="orange"
          />

          <GlassCard
            icon={<Flame className="w-8 h-8 text-neon-amber" />}
            title="Blazing Performance"
            description="Optimized for maximum throughput and minimal latency"
            glowColor="amber"
          />
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative z-10 container mx-auto px-4 py-20">
        <div className="glass-card p-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-5xl font-bold neon-text text-glow">99.9%</div>
              <div className="text-gray-400 uppercase tracking-wider">Uptime</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold neon-text text-glow">10M+</div>
              <div className="text-gray-400 uppercase tracking-wider">Requests/Day</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold neon-text text-glow">&lt;5ms</div>
              <div className="text-gray-400 uppercase tracking-wider">Latency</div>
            </div>
            <div className="space-y-2">
              <div className="text-5xl font-bold neon-text text-glow">24/7</div>
              <div className="text-gray-400 uppercase tracking-wider">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 container mx-auto px-4 py-20 text-center">
        <div className="glass-card p-12 max-w-4xl mx-auto space-y-6">
          <h2 className="text-4xl md:text-5xl font-bold neon-text">
            Ready to Experience the Future?
          </h2>
          <p className="text-xl text-gray-400">
            Join thousands of developers building the next generation of AI applications
          </p>
          <NeonButton variant="primary" size="lg">
            <Flame className="w-6 h-6 mr-2" />
            Get Started Now
          </NeonButton>
        </div>
      </section>

      <Footer />
    </main>
  )
}
