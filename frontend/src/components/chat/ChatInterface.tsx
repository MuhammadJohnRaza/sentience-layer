/** * Main Chat Interface */ "use client";
import { useRef, useEffect } from "react";
import { useChat } from "@/hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedActions } from "./SuggestedActions";
import { VoiceInput } from "./VoiceInput";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
export function ChatInterface() {
  const { messages, isLoading, sendMessage, clearChat } = useChat();
  const inputRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const content = inputRef.current?.value.trim();
    if (!content || isLoading) return;
    sendMessage(content);
    inputRef.current!.value = "";
  };
  return (
    <div className="flex h-full flex-col rounded-xl border bg-white dark:bg-background">
      {" "}
      <div className="flex items-center justify-between border-b p-4">
        {" "}
        <div>
          {" "}
          <h2 className="font-semibold">Sentience Chat</h2>{" "}
          <p className="text-xs text-foreground0">
            Multi-agent reasoning engine
          </p>{" "}
        </div>{" "}
        <Button variant="ghost" size="sm" onClick={clearChat}>
          {" "}
          Clear{" "}
        </Button>{" "}
      </div>{" "}
      <ScrollArea className="flex-1 p-4">
        {" "}
        <div className="space-y-4">
          {" "}
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              {" "}
              <div className="h-12 w-12 rounded-full bg-border/10 dark:bg-border/30 mb-4" />{" "}
              <p className="text-foreground0">
                Start a conversation with the Sentience Layer
              </p>{" "}
            </div>
          )}
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={bottomRef} />{" "}
        </div>{" "}
      </ScrollArea>{" "}
      <div className="border-t p-4">
        {" "}
        <SuggestedActions onAction={sendMessage} />{" "}
        <form onSubmit={handleSubmit} className="mt-3 flex items-center gap-2">
          {" "}
          <VoiceInput
            onTranscript={(text) => {
              if (inputRef.current) inputRef.current.value = text;
            }}
          />{" "}
          <Input
            ref={inputRef}
            placeholder="Ask anything..."
            className="flex-1"
            disabled={isLoading}
          />{" "}
          <Button type="submit" disabled={isLoading}>
            {" "}
            Send{" "}
          </Button>{" "}
        </form>{" "}
      </div>{" "}
    </div>
  );
}
