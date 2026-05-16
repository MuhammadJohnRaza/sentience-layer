/**
 * Typing Indicator — Black / Purple / Gold Theme
 */

export function TypingIndicator() {
  return (
    <div className="flex gap-3 justify-start">
      {/* Avatar */}
      <div className="flex-shrink-0 h-8 w-8 rounded-full bg-purple-900/40 border border-[#EAB308]/40 flex items-center justify-center">
        <div className="h-2 w-2 rounded-full bg-[#EAB308] animate-pulse" />
      </div>

      <div className="flex flex-col gap-1 items-start">
        <span className="text-[10px] font-medium uppercase tracking-wider text-[#A855F7]/60">
          Sentience AI
        </span>
        <div className="flex items-center gap-3 rounded-2xl rounded-bl-sm bg-zinc-900/80 border border-zinc-700/50 px-4 py-3">
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-[#A855F7] animate-bounce [animation-delay:-0.3s]" />
            <span className="h-2 w-2 rounded-full bg-[#A855F7] animate-bounce [animation-delay:-0.15s]" />
            <span className="h-2 w-2 rounded-full bg-[#A855F7] animate-bounce" />
          </div>
          <span className="text-xs text-[#A855F7]/60 animate-pulse">Cognitive agents are reasoning...</span>
        </div>
      </div>
    </div>
  );
}