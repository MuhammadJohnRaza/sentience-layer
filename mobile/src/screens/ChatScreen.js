import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, View, ScrollView, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { ChatBubble } from '../components/ChatBubble';
import { TypingIndicator } from '../components/TypingIndicator';
import { SuggestedActions } from '../components/SuggestedActions';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function ChatScreen() {
  const theme = useTheme();
  const scrollViewRef = useRef(null);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      isAgent: true,
      agentName: 'COGNITIVE KERNEL',
      text: 'Multi-agent reasoning kernel active. Connect your thoughts with the Sentience Layer cognitive architecture.',
      confidence: 0.98
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const sendMessage = (text) => {
    const messageText = text || inputText;
    if (!messageText.trim()) return;

    const newMsg = { id: Date.now(), isAgent: false, text: messageText };
    setMessages([...messages, newMsg]);
    setInputText('');
    setIsTyping(true);

    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        isAgent: true,
        agentName: 'COGNITIVE KERNEL',
        text: 'Understood. Dispatching causal inference agents to map the requested objective and simulate downstream effects.',
        confidence: 0.95
      }]);
    }, 2000);
  };

  return (
    <ScreenWrapper>
      <TopBar
        title="SENTIENCE COGNITIVE CHAT"
        subtitle="🧠 Multi-Agent Reasoning Kernel Active"
        showStatus={true}
      />

      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        {/* Messages Area */}
        <ScrollView
          ref={scrollViewRef}
          contentContainerStyle={styles.chatScroll}
          style={styles.scrollView}
        >
          {messages.length === 0 && (
            <View style={styles.emptyState}>
              <View style={[styles.emptyIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.1)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 32 }}>🔮</Typography>
              </View>
              <Typography variant="h3" uppercase style={styles.emptyTitle}>
                Initialize Communication
              </Typography>
              <Typography variant="body" style={styles.emptyText}>
                Connect your thoughts with the Sentience Layer multi-agent cognitive architecture. Begin typing to prompt the kernel.
              </Typography>
            </View>
          )}

          {messages.map(msg => (
            <ChatBubble
              key={msg.id}
              isAgent={msg.isAgent}
              agentName={msg.agentName}
              message={msg.text}
              confidence={msg.confidence}
            />
          ))}
          {isTyping && <TypingIndicator />}
        </ScrollView>

        {/* Input Area */}
        <View style={[styles.inputContainer, {
          backgroundColor: 'rgba(17, 17, 17, 0.95)',
          borderTopColor: theme.colors.border,
        }]}>
          <SuggestedActions onAction={sendMessage} />

          <View style={styles.inputRow}>
            <TouchableOpacity style={[styles.iconBtn, {
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              borderColor: theme.colors.border,
            }]}>
              <Typography style={{ fontSize: 18 }}>📎</Typography>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.iconBtn, {
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              borderColor: theme.colors.border,
            }]}>
              <Typography style={{ fontSize: 18 }}>🎤</Typography>
            </TouchableOpacity>

            <TextInput
              style={[styles.input, {
                color: theme.colors.textBody,
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                borderColor: theme.colors.border,
              }]}
              placeholder="Prompt the core network..."
              placeholderTextColor={theme.colors.textMuted}
              value={inputText}
              onChangeText={setInputText}
              multiline
            />

            <Button
              variant="primary"
              size="icon"
              onPress={() => sendMessage()}
              disabled={isTyping}
              style={styles.sendBtn}
            >
              <Typography style={{ fontSize: 20 }}>🚀</Typography>
            </Button>
          </View>
        </View>
      </KeyboardAvoidingView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.25)',
  },
  chatScroll: {
    padding: 16,
    paddingBottom: 40,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 80,
    paddingHorizontal: 32,
  },
  emptyIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  emptyTitle: {
    marginBottom: 12,
    textAlign: 'center',
  },
  emptyText: {
    textAlign: 'center',
    lineHeight: 22,
  },
  inputContainer: {
    borderTopWidth: 1,
    padding: 12,
    gap: 12,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
  },
  iconBtn: {
    width: 40,
    height: 40,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  input: {
    flex: 1,
    fontSize: 14,
    fontWeight: '600',
    letterSpacing: 0.5,
    minHeight: 40,
    maxHeight: 100,
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 12,
    borderRadius: 12,
    borderWidth: 1,
  },
  sendBtn: {
    width: 44,
    height: 44,
  },
});
