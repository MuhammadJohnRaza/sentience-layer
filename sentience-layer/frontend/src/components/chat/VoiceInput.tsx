/**
 * Voice Input Button
 */

"use client";

import { useVoiceInput } from "@/hooks/useVoiceInput";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function VoiceInput({ onTranscript }: { onTranscript: (text: string) => void }) {
  const { isListening, transcript, startListening, stopListening, isSupported } = useVoiceInput();

  if (!isSupported) return null;

  return (
    <Button
      type="button"
      variant="ghost"
      size="icon"
      onClick={isListening ? stopListening : startListening}
      className={cn(
        "relative",
        isListening && "text-red-500 animate-pulse"
      )}
    >
      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
      </svg>
      {transcript && onTranscript(transcript)}
    </Button>
  );
}