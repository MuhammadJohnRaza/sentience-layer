import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Hexagon, User } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';
const TEXT_MUTED = '#A7A7B5';

export function ChatBubble({ message, isAgent = true, agentName = 'KERNEL' }) {
  return (
    <View style={[styles.container, isAgent ? styles.agentContainer : styles.userContainer]}>
      {isAgent && (
        <View style={styles.avatar}>
          <Hexagon color={PRIMARY_NEON} size={16} />
        </View>
      )}
      <View style={[styles.bubble, isAgent ? styles.agentBubble : styles.userBubble]}>
        {isAgent && <Text style={styles.agentName}>{agentName}</Text>}
        <Text style={styles.messageText}>{message}</Text>
      </View>
      {!isAgent && (
        <View style={[styles.avatar, styles.userAvatar]}>
          <User color={TEXT_MUTED} size={16} />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginBottom: 16,
    maxWidth: '85%',
  },
  agentContainer: {
    alignSelf: 'flex-start',
  },
  userContainer: {
    alignSelf: 'flex-end',
    justifyContent: 'flex-end',
  },
  avatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: 'rgba(122, 46, 255, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
  },
  userAvatar: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    marginLeft: 8,
  },
  bubble: {
    padding: 12,
    borderRadius: 16,
    marginLeft: isAgent => (isAgent ? 8 : 0),
  },
  agentBubble: {
    backgroundColor: 'rgba(122, 46, 255, 0.08)',
    borderTopLeftRadius: 4,
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.2)',
  },
  userBubble: {
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    borderTopRightRadius: 4,
  },
  agentName: {
    color: PRIMARY_NEON,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
    marginBottom: 4,
  },
  messageText: {
    color: TEXT_HIGHLIGHT,
    fontSize: 14,
    lineHeight: 20,
  }
});
