import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useTheme } from '../hooks/useTheme';

export const Card = ({ children, style }) => {
  const theme = useTheme();

  return (
    <View style={[
      styles.card, 
      { 
        backgroundColor: theme.colors.surface, 
        borderColor: theme.colors.border,
        borderRadius: theme.borderRadius.lg 
      }, 
      style
    ]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderWidth: 1,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
});
