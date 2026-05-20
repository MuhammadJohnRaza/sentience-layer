import React from 'react';
import { Text, StyleSheet } from 'react-native';
import { useTheme } from '../hooks/useTheme';

export function Typography({ variant = 'body', children, style, uppercase, ...props }) {
  const theme = useTheme();

  const getVariantStyle = () => {
    switch (variant) {
      case 'h1':
        return {
          fontSize: 28,
          fontWeight: '800',
          color: theme.colors.textHighlight,
          letterSpacing: 2,
          textShadowColor: 'rgba(252, 211, 77, 0.3)',
          textShadowOffset: { width: 0, height: 0 },
          textShadowRadius: 10,
        };
      case 'h2':
        return {
          fontSize: 20,
          fontWeight: '800',
          color: theme.colors.textHighlight,
          letterSpacing: 2,
        };
      case 'h3':
        return {
          fontSize: 16,
          fontWeight: '700',
          color: theme.colors.textHighlight,
          letterSpacing: 1.5,
        };
      case 'body':
        return {
          fontSize: 14,
          fontWeight: '500',
          color: theme.colors.textBody,
          lineHeight: 22,
          letterSpacing: 0.5,
        };
      case 'bodyBold':
        return {
          fontSize: 14,
          fontWeight: '700',
          color: theme.colors.textBody,
          lineHeight: 22,
          letterSpacing: 0.8,
        };
      case 'caption':
        return {
          fontSize: 11,
          fontWeight: '700',
          color: theme.colors.textMuted,
          letterSpacing: 1,
        };
      case 'tiny':
        return {
          fontSize: 9,
          fontWeight: '800',
          color: theme.colors.textMuted,
          letterSpacing: 1.5,
        };
      case 'button':
        return {
          fontSize: 12,
          fontWeight: '800',
          color: theme.colors.textHighlight,
          letterSpacing: 1.5,
        };
      case 'neonText':
        return {
          fontSize: 14,
          fontWeight: '700',
          color: theme.colors.primaryNeon,
          textShadowColor: theme.colors.primaryGlow,
          textShadowOffset: { width: 0, height: 0 },
          textShadowRadius: 8,
          letterSpacing: 0.8,
        };
      default:
        return {
          fontSize: 14,
          fontWeight: '500',
          color: theme.colors.textBody,
          letterSpacing: 0.5,
        };
    }
  };

  const content = uppercase && typeof children === 'string' ? children.toUpperCase() : children;

  return (
    <Text style={[getVariantStyle(), style]} {...props}>
      {content}
    </Text>
  );
}

