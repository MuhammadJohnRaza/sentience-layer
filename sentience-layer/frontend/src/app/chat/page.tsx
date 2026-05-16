/**
 * Chat Interface Page — Full height immersive layout
 */

"use client";

import { ChatInterface } from "@/components/chat/ChatInterface";

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-4rem)] -m-6">
      <ChatInterface />
    </div>
  );
}