import { useColorScheme } from 'react-native';

export function useTheme() {
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === 'dark' || true; // Enforce dark mode for Sentience

  return {
    isDarkMode,
    colors: {
      background: '#050505',
      surface: '#0B0B12',
      border: 'rgba(122, 46, 255, 0.15)',
      backgroundPrimary: '#050505',
      backgroundSecondary: '#0B0B12',
      primaryNeon: '#7A2EFF',
      primaryGlow: '#9B5CFF',
      accentGold: '#F6C344',
      textMuted: '#A7A7B5',
      textHighlight: '#F5F5F7',
      danger: '#FF453A',
      success: '#32D74B',
      borderLight: 'rgba(122, 46, 255, 0.15)',
      borderMedium: 'rgba(122, 46, 255, 0.3)',
    },
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 12,
      xl: 16,
    }
  };
}
