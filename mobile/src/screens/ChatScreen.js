import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TextInput, TouchableOpacity } from 'react-native';
import { Rocket } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { ChatBubble } from '../components/ChatBubble';
import { TypingIndicator } from '../components/TypingIndicator';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function ChatScreen() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([
    { id: 1, isAgent: true, agentName: 'KERNEL', text: 'Multi-agent reasoning active. State your objective.' }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = () => {
    if (!inputText.trim()) return;
    const newMsg = { id: Date.now(), isAgent: false, text: inputText };
    setMessages([...messages, newMsg]);
    setInputText('');
    setIsTyping(true);

    // Simulate agent response
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { id: Date.now() + 1, isAgent: true, agentName: 'KERNEL', text: 'Understood. Dispatching causal inference agents to map the requested objective.' }]);
    }, 2000);
  };

  return (
    <ScreenWrapper>
      <TopBar title="COGNITIVE CHAT" />
      <View style={styles.container}>
        <ScrollView contentContainerStyle={styles.chatScroll}>
          {messages.map(msg => (
            <ChatBubble key={msg.id} isAgent={msg.isAgent} agentName={msg.agentName} message={msg.text} />
          ))}
          {isTyping && <TypingIndicator />}
        </ScrollView>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Prompt the core network..."
            placeholderTextColor="#A7A7B5"
            value={inputText}
            onChangeText={setInputText}
            multiline
          />
          <TouchableOpacity style={styles.sendBtn} onPress={sendMessage}>
            <Rocket color={TEXT_HIGHLIGHT} size={20} />
          </TouchableOpacity>
        </View>
      </View>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  chatScroll: { padding: 16, paddingBottom: 40 },
  inputContainer: { flexDirection: 'row', alignItems: 'flex-end', padding: 12, backgroundColor: 'rgba(255,255,255,0.02)', borderTopWidth: 1, borderTopColor: 'rgba(122,46,255,0.15)' },
  input: { flex: 1, color: TEXT_HIGHLIGHT, fontSize: 14, minHeight: 40, maxHeight: 100, paddingHorizontal: 16, paddingTop: 12, paddingBottom: 12, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 20 },
  sendBtn: { width: 44, height: 44, borderRadius: 22, backgroundColor: PRIMARY_NEON, justifyContent: 'center', alignItems: 'center', marginLeft: 12, shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 10, elevation: 5 }
});
