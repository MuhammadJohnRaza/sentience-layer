/**
 * Application Constants
 */

export const APP_NAME = "Sentience Layer";
export const APP_VERSION = "4.0.0";
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

export const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", icon: "LayoutDashboard" },
  { label: "Chat", href: "/chat", icon: "MessageSquare" },
  { label: "Wins", href: "/win", icon: "Trophy" },
  { label: "Actions", href: "/action", icon: "Zap" },
  { label: "Playbooks", href: "/playbook", icon: "BookOpen" },
  { label: "Vault", href: "/vault", icon: "Shield" },
  { label: "Memory", href: "/memory", icon: "Brain" },
  { label: "Trace", href: "/trace", icon: "GitBranch" },
  { label: "Simulate", href: "/simulate", icon: "FlaskConical" },
  { label: "Mission Control", href: "/mission-control", icon: "Rocket" },
  { label: "Causal Explorer", href: "/causal-explorer", icon: "Network" },
  { label: "Economic Model", href: "/economic-model", icon: "TrendingUp" },
  { label: "Dreamscape", href: "/dreamscape", icon: "Moon" },
  { label: "Doubt Room", href: "/doubt-room", icon: "HelpCircle" },
  { label: "Mirror", href: "/mirror", icon: "UserCircle" },
];

export const AGENT_TYPES = [
  { id: "personalization", name: "Personalization", color: "#8b5cf6" },
  { id: "memory", name: "Memory", color: "#06b6d4" },
  { id: "deterministic", name: "Deterministic", color: "#10b981" },
  { id: "ranking", name: "Action Ranking", color: "#f59e0b" },
  { id: "priority", name: "Priority", color: "#ef4444" },
  { id: "opportunity", name: "Opportunity", color: "#ec4899" },
  { id: "causal", name: "Causal Inference", color: "#6366f1" },
  { id: "adversarial", name: "Red Team", color: "#dc2626" },
  { id: "debate", name: "Debate", color: "#d946ef" },
  { id: "critic", name: "Critic", color: "#f97316" },
  { id: "consensus", name: "Consensus", color: "#14b8a6" },
  { id: "uncertainty", name: "Uncertainty", color: "#64748b" },
  { id: "economic", name: "Economic", color: "#84cc16" },
  { id: "dream", name: "Dream", color: "#a855f7" },
  { id: "premonition", name: "Premonition", color: "#e11d48" },
  { id: "ethics", name: "Ethics", color: "#fbbf24" },
];

export const SIMULATION_STATUS = {
  pending: { label: "Pending", color: "bg-slate-500" },
  running: { label: "Running", color: "bg-blue-500" },
  completed: { label: "Completed", color: "bg-emerald-500" },
  failed: { label: "Failed", color: "bg-red-500" },
};