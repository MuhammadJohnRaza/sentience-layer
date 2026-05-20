import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useTheme } from '../hooks/useTheme';

export const Card = ({ children, style, variant = 'default' }) => {
  const theme = useTheme();

  const getVariantStyle = () => {
    switch (variant) {
      case 'elevated':
        return {
          borderWidth: 2,
          borderColor: 'rgba(124, 58, 237, 0.4)',
          ...theme.shadows.panelShadow,
        };
      case 'glow':
        return {
          borderWidth: 2,
          borderColor: theme.colors.borderMedium,
          ...theme.shadows.neonGlow,
        };
      default:
        return {
          borderWidth: 2,
          borderColor: theme.colors.border,
          ...theme.shadows.cardShadow,
        };
    }
  };

  return (
    <View style={[
      styles.card,
      {
        backgroundColor: theme.colors.card,
        borderRadius: theme.borderRadius.lg,
      },
      getVariantStyle(),
      style
    ]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 16,
    marginVertical: 8,
  },
});
