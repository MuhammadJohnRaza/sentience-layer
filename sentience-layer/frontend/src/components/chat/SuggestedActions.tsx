/**
 * Suggested Actions — Black / Purple / Gold Theme
 */

"use client";

const SUGGESTIONS = [
  { label: "Analyze resource allocation", icon: "⚡" },
  { label: "Run opportunity scan", icon: "🔍" },
  { label: "Show causal graph", icon: "🧠" },
  { label: "Simulate intervention", icon: "🎯" },
  { label: "Check system health", icon: "💚" },
  { label: "Extract latest insights", icon: "✨" },
];

export function SuggestedActions({ onAction }: { onAction: (text: string) => void }) {
  return (
    <div className="flex flex-wrap gap-2">
      {SUGGESTIONS.map((s) => (
        <button
          key={s.label}
          onClick={() => onAction(s.label)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs border border-zinc-800 text-[#A855F7] bg-purple-900/10 hover:bg-purple-900/30 hover:border-[#A855F7]/50 hover:text-[#EAB308] transition-all"
        >
          <span>{s.icon}</span>
          <span>{s.label}</span>
        </button>
      ))}
    </div>
  );
}