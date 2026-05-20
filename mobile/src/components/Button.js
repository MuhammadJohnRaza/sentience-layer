import React from 'react';
import { TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

export function Button({
  children,
  onPress,
  variant = 'primary',
  size = 'default',
  disabled = false,
  loading = false,
  style,
  textStyle,
  icon,
  ...props
}) {
  const theme = useTheme();

  const getVariantStyle = () => {
    switch (variant) {
      case 'primary':
        return {
          backgroundColor: 'rgba(124, 58, 237, 0.2)',
          borderColor: theme.colors.border,
          borderWidth: 2,
          ...theme.shadows.buttonGlow,
        };
      case 'secondary':
        return {
          backgroundColor: 'rgba(0, 0, 0, 0.4)',
          borderColor: theme.colors.border,
          borderWidth: 1,
        };
      case 'outline':
        return {
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          borderColor: 'rgba(124, 58, 237, 0.3)',
          borderWidth: 1,
        };
      case 'ghost':
        return {
          backgroundColor: 'transparent',
          borderColor: 'transparent',
          borderWidth: 0,
        };
      case 'destructive':
        return {
          backgroundColor: 'rgba(239, 68, 68, 0.2)',
          borderColor: 'rgba(239, 68, 68, 0.3)',
          borderWidth: 2,
        };
      default:
        return {
          backgroundColor: 'rgba(124, 58, 237, 0.2)',
          borderColor: theme.colors.border,
          borderWidth: 2,
        };
    }
  };

  const getSizeStyle = () => {
    switch (size) {
      case 'sm':
        return {
          paddingHorizontal: 12,
          paddingVertical: 6,
          borderRadius: theme.borderRadius.md,
        };
      case 'lg':
        return {
          paddingHorizontal: 24,
          paddingVertical: 14,
          borderRadius: theme.borderRadius.lg,
        };
      case 'icon':
        return {
          width: 44,
          height: 44,
          borderRadius: theme.borderRadius.full,
          padding: 0,
        };
      default:
        return {
          paddingHorizontal: 16,
          paddingVertical: 10,
          borderRadius: theme.borderRadius.md,
        };
    }
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled || loading}
      style={[
        styles.button,
        getVariantStyle(),
        getSizeStyle(),
        (disabled || loading) && styles.disabled,
        style,
      ]}
      activeOpacity={0.7}
      {...props}
    >
      {loading ? (
        <ActivityIndicator color={theme.colors.textHighlight} size="small" />
      ) : (
        <>
          {icon && <>{icon}</>}
          {typeof children === 'string' ? (
            <Typography variant="button" uppercase style={[styles.text, textStyle]}>
              {children}
            </Typography>
          ) : (
            children
          )}
        </>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  text: {
    textAlign: 'center',
  },
  disabled: {
    opacity: 0.5,
  },
});
