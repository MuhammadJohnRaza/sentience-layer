import React, { useState } from 'react';
import { StyleSheet, View, TouchableOpacity } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';
import { Button } from './Button';

export function ChatBubble({ message, isAgent = true, agentName = 'COGNITIVE KERNEL', confidence }) {
  const theme = useTheme();
  const [isLoved, setIsLoved] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  return (
    <View style={[styles.container, isAgent ? styles.agentContainer : styles.userContainer]}>
      {/* Avatar */}
      <View style={[
        styles.avatar,
        {
          backgroundColor: isAgent ? 'rgba(245, 158, 11, 0.2)' : 'rgba(124, 58, 237, 0.2)',
          borderColor: isAgent ? 'rgba(245, 158, 11, 0.3)' : theme.colors.border,
          borderWidth: 2,
        },
        isAgent && {
          shadowColor: '#F59E0B',
          shadowOffset: { width: 0, height: 0 },
          shadowOpacity: 0.25,
          shadowRadius: 12,
          elevation: 5,
        }
      ]}>
        <Typography style={{ fontSize: 16 }}>
          {isAgent ? '🧠' : '👤'}
        </Typography>
      </View>

      {/* Message Bubble */}
      <View style={[
        styles.bubble,
        {
          backgroundColor: isAgent ? theme.colors.card : 'rgba(124, 58, 237, 0.1)',
          borderColor: isAgent ? 'rgba(124, 58, 237, 0.2)' : 'rgba(124, 58, 237, 0.6)',
          borderWidth: 1,
          borderRadius: 16,
          shadowColor: '#000000',
          shadowOffset: { width: 0, height: 4 },
          shadowOpacity: isAgent ? 0.6 : 0.15,
          shadowRadius: 15,
          elevation: isAgent ? 8 : 4,
        },
        isAgent ? { borderTopLeftRadius: 4 } : { borderTopRightRadius: 4 }
      ]}>
        {/* Header */}
        <View style={styles.header}>
          <Typography variant="tiny" uppercase style={{
            color: isAgent ? '#FCD34D' : theme.colors.textHighlight
          }}>
            {isAgent ? agentName : 'USER COGNITION'}
          </Typography>
          {confidence && (
            <View style={[styles.badge, {
              backgroundColor: 'rgba(16, 185, 129, 0.2)',
              borderColor: 'rgba(16, 185, 129, 0.25)',
            }]}>
              <Typography variant="tiny" style={{ color: '#10B981' }}>
                {Math.round(confidence * 100)}% CONFIDENCE
              </Typography>
            </View>
          )}
        </View>

        {/* Message Content */}
        <Typography variant="body" style={styles.messageText}>
          {message}
        </Typography>

        {/* Action Buttons (Agent only) */}
        {isAgent && (
          <View style={styles.actions}>
            <TouchableOpacity
              onPress={() => setIsSaved(!isSaved)}
              style={[styles.actionBtn, {
                backgroundColor: isSaved ? 'rgba(16, 185, 129, 0.2)' : 'rgba(0, 0, 0, 0.4)',
                borderColor: isSaved ? 'rgba(16, 185, 129, 0.4)' : theme.colors.border,
              }]}
            >
              <Typography variant="tiny" uppercase style={{
                color: isSaved ? '#10B981' : theme.colors.textMuted
              }}>
                {isSaved ? '🔒 SAVED' : '💾 SAVE'}
              </Typography>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => setIsLoved(!isLoved)}
              style={[styles.actionBtn, {
                backgroundColor: isLoved ? 'rgba(244, 63, 94, 0.2)' : 'rgba(0, 0, 0, 0.4)',
                borderColor: isLoved ? 'rgba(244, 63, 94, 0.4)' : theme.colors.border,
                paddingHorizontal: 10,
              }]}
            >
              <Typography style={{ fontSize: 14 }}>
                {isLoved ? '❤️' : '🤍'}
              </Typography>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginBottom: 16,
    maxWidth: '85%',
    gap: 12,
  },
  agentContainer: {
    alignSelf: 'flex-start',
  },
  userContainer: {
    alignSelf: 'flex-end',
    flexDirection: 'row-reverse',
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
  },
  bubble: {
    flex: 1,
    padding: 14,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 8,
    gap: 8,
  },
  badge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
    borderWidth: 1,
  },
  messageText: {
    lineHeight: 22,
  },
  actions: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(124, 58, 237, 0.1)',
  },
  actionBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
  },
});
