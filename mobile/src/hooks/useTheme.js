import { useColorScheme } from 'react-native';
import { theme } from '../utils/theme';

export function useTheme() {
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === 'dark' || true; // Enforce dark mode for Sentience

  return {
    isDarkMode,
    colors: {
      ...theme.colors,
      background: theme.colors.backgroundPrimary,
      surface: theme.colors.backgroundSecondary,
      border: theme.colors.borderLight,
    },
    shadows: theme.shadows,
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 12,
      xl: 16,
    }
  };
}
