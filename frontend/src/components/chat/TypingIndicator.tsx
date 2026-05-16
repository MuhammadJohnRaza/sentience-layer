/** * Typing Animation */
export function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 rounded-2xl bg-border/10 px-4 py-3 dark:bg-border/30 w-fit">
      {" "}
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />{" "}
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />{" "}
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />{" "}
      <span className="ml-2 text-xs text-foreground0">
        Agents are reasoning...
      </span>{" "}
    </div>
  );
}
