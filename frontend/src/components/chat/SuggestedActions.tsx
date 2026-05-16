/** * Suggested Actions Chips */ "use client";
import { Button } from "@/components/ui/button";
const SUGGESTIONS = [
  "Analyze my recent actions",
  "Run opportunity scan",
  "Show causal graph",
  "Start dream consolidation",
  "Check system health",
];
export function SuggestedActions({
  onAction,
}: {
  onAction: (text: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {" "}
      {SUGGESTIONS.map((suggestion) => (
        <Button
          key={suggestion}
          variant="outline"
          size="sm"
          className="text-xs rounded-full"
          onClick={() => onAction(suggestion)}
        >
          {" "}
          {suggestion}
        </Button>
      ))}
    </div>
  );
}
