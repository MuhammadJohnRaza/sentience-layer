"use client";

import { Button } from "@/components/ui/button";

const SUGGESTIONS = [
  "🔍 Analyze recent actions",
  "🔮 Run opportunity scan",
  "🕸️ Show causal graph",
  "🌌 Start dream consolidation",
  "❤️ Check system health",
];

export function SuggestedActions({
  suggestions,
  onAction,
}: {
  suggestions?: string[];
  onAction: (text: string) => void;
}) {
  const activeSuggestions = suggestions && suggestions.length > 0 ? suggestions : SUGGESTIONS;
  return (
    <div className="flex flex-wrap gap-2 py-1">
      {activeSuggestions.map((suggestion) => (
        <Button
          key={suggestion}
          variant="outline"
          size="sm"
          className="text-xs rounded-full border border-border/30 bg-background/50 hover:bg-primary/20 hover:text-primary-foreground hover:border-border hover:shadow-[0_0_12px_rgba(124,58,237,0.3)] transition-all duration-300 font-semibold tracking-wide"
          onClick={() => onAction(suggestion)}
        >
          {suggestion}
        </Button>
      ))}
    </div>
  );
}
