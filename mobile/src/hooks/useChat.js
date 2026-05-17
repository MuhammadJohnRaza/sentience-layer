import { useState, useCallback } from 'react';
import { openRouterService } from '../services/openrouter';

export function useChat() {
  const [messages, setMessages] = useState([
    { id: '1', isAgent: true, agentName: 'KERNEL', text: 'Multi-agent reasoning active. State your objective.' }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = useCallback(async (text) => {
    if (!text.trim()) return;

    const userMsg = { id: Date.now().toString(), isAgent: false, text };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    try {
      // Connect to the actual backend LLM router
      const response = await openRouterService.sendPrompt(text);
      
      const agentMsg = {
        id: (Date.now() + 1).toString(),
        isAgent: true,
        agentName: response.agent || 'KERNEL',
        text: response.reply || response.response || JSON.stringify(response)
      };
      setMessages(prev => [...prev, agentMsg]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        isAgent: true,
        agentName: 'SYSTEM_ERROR',
        text: 'Failed to reach reasoning kernel. Ensure backend is running.'
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  }, []);

  const clearChat = useCallback(() => {
    setMessages([{ id: Date.now().toString(), isAgent: true, agentName: 'KERNEL', text: 'Memory cleared. Ready for new objective.' }]);
  }, []);

  return { messages, isTyping, sendMessage, clearChat };
}
