import React from 'react';
import { Text, StyleSheet } from 'react-native';

export function Typography({ variant = 'body', children, style, ...props }) {
  return (
    <Text style={[styles[variant], style]} {...props}>
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  h1: {
    fontSize: 28,
    fontWeight: '800',
    color: '#F5F5F7',
    letterSpacing: 2,
    textShadowColor: 'rgba(245, 245, 247, 0.3)',
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 10,
  },
  h2: {
    fontSize: 20,
    fontWeight: '700',
    color: '#F5F5F7',
    letterSpacing: 1.5,
  },
  body: {
    fontSize: 14,
    color: '#A7A7B5',
    lineHeight: 22,
  },
  caption: {
    fontSize: 11,
    color: '#A7A7B5',
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  neonText: {
    fontSize: 14,
    color: '#7A2EFF',
    fontWeight: '700',
    textShadowColor: '#9B5CFF',
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 8,
  }
});
