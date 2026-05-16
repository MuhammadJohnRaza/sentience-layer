/**
 * Message Bubble — Black / Purple / Gold Theme
 */

import { Message } from "@/types";
import { cn } from "@/lib/utils";

function formatTime(iso: string) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  const isAssistant = message.role === "assistant";

  return (
    <div className={cn("flex gap-3", isUser ? "justify-end" : "justify-start")}>
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-purple-900/40 border border-[#EAB308]/40 flex items-center justify-center mt-1">
          <div className="h-2 w-2 rounded-full bg-[#EAB308]" />
        </div>
      )}

      <div className={cn("flex flex-col gap-1", isUser ? "items-end" : "items-start", "max-w-[78%]")}>
        {/* Role label */}
        <span className={cn("text-[10px] font-medium uppercase tracking-wider", isUser ? "text-[#EAB308]/60" : "text-[#A855F7]/60")}>
          {isUser ? "You" : isSystem ? "System" : "Sentience AI"}
        </span>

        {/* Bubble */}
        <div className={cn(
          "rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-gradient-to-br from-purple-900/60 to-purple-900/30 border border-[#A855F7]/30 text-slate-100 rounded-br-sm"
            : isSystem
            ? "bg-red-950/40 border border-red-800/40 text-red-300 rounded-bl-sm"
            : "bg-zinc-900/80 border border-zinc-700/50 text-slate-100 rounded-bl-sm"
        )}>
          {/* Content with preserved line breaks */}
          <p className="whitespace-pre-wrap break-words">{message.content}</p>

          {/* Suggested actions from AI response */}
          {isAssistant && message.metadata?.actions && message.metadata.actions.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1.5 pt-3 border-t border-zinc-700/50">
              <p className="w-full text-[10px] text-[#A855F7]/60 mb-1 uppercase tracking-wide">Suggested Actions</p>
              {message.metadata.actions.map((action: any, i: number) => (
                <span
                  key={action.id || i}
                  className="px-2 py-1 rounded-full text-[11px] bg-purple-900/30 border border-[#A855F7]/30 text-[#A855F7] cursor-pointer hover:bg-purple-900/50 hover:text-[#EAB308] transition-colors"
                >
                  {action.title || action}
                </span>
              ))}
            </div>
          )}

          {/* Sources */}
          {isAssistant && message.metadata?.sources && message.metadata.sources.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1 pt-2 border-t border-zinc-700/40">
              <span className="text-[10px] text-zinc-600 w-full">Sources:</span>
              {message.metadata.sources.slice(0, 3).map((src: string, i: number) => (
                <span key={i} className="text-[10px] text-zinc-500 bg-zinc-800/60 rounded px-1.5 py-0.5">
                  {src}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Timestamp + confidence */}
        <div className={cn("flex items-center gap-2 text-[10px]", isUser ? "text-zinc-600" : "text-zinc-600")}>
          <span>{formatTime(message.timestamp)}</span>
          {message.metadata?.confidence && (
            <>
              <span className="text-zinc-800">·</span>
              <span className="text-[#A855F7]/60">
                {(message.metadata.confidence * 100).toFixed(0)}% confidence
              </span>
            </>
          )}
          {message.metadata?.intent && (
            <>
              <span className="text-zinc-800">·</span>
              <span className="text-zinc-600 capitalize">{message.metadata.intent}</span>
            </>
          )}
        </div>
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-[#EAB308]/20 border border-[#EAB308]/40 flex items-center justify-center mt-1">
          <svg className="h-4 w-4 text-[#EAB308]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
      )}
    </div>
  );
}