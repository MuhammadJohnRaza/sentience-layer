import React from 'react';
import { StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

const SUGGESTIONS = [
  '🔍 Analyze recent actions',
  '🔮 Run opportunity scan',
  '🕸️ Show causal graph',
  '🌌 Start dream consolidation',
  '❤️ Check system health',
];

export function SuggestedActions({ onAction }) {
  const theme = useTheme();

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.container}
    >
      {SUGGESTIONS.map((suggestion, index) => (
        <TouchableOpacity
          key={index}
          onPress={() => onAction && onAction(suggestion)}
          style={[styles.chip, {
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            borderColor: 'rgba(124, 58, 237, 0.3)',
          }]}
          activeOpacity={0.7}
        >
          <Typography variant="caption" style={styles.chipText}>
            {suggestion}
          </Typography>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: 8,
    paddingVertical: 4,
  },
  chip: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
  },
  chipText: {
    fontWeight: '700',
    letterSpacing: 0.8,
  },
});
