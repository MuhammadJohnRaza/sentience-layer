import React from 'react';
import { Text, StyleSheet } from 'react-native';
import { useTheme } from '../hooks/useTheme';

export const Typography = ({ children, variant = 'body', style, ...props }) => {
  const theme = useTheme();

  const getVariantStyle = () => {
    switch (variant) {
      case 'h1':
        return {
          fontSize: 32,
          fontWeight: 'bold',
          color: theme.colors.primary, // Purple for headings
          marginBottom: 16,
        };
      case 'h2':
        return {
          fontSize: 24,
          fontWeight: 'bold',
          color: theme.colors.primary,
          marginBottom: 12,
        };
      case 'h3':
        return {
          fontSize: 20,
          fontWeight: '600',
          color: theme.colors.primary,
          marginBottom: 8,
        };
      case 'body':
      default:
        return {
          fontSize: 16,
          color: theme.colors.text, // Gold/Yellow as in frontend
        };
      case 'muted':
        return {
          fontSize: 14,
          color: theme.colors.textMuted,
        };
      case 'purple':
        return {
          fontSize: 16,
          color: theme.colors.primary,
        };
    }
  };

  return (
    <Text style={[getVariantStyle(), style]} {...props}>
      {children}
    </Text>
  );
};
