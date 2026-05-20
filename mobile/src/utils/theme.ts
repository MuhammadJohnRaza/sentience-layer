export const theme = {
  colors: {
    backgroundPrimary: '#000000',
    backgroundSecondary: '#111111',
    primaryNeon: '#7C3AED',
    primaryGlow: '#A855F7',
    accentGold: '#FCD34D',
    textBody: '#FDE68A',
    textMuted: '#D4D4D8',
    textHighlight: '#FCD34D',
    danger: '#EF4444',
    success: '#22C55E',
    borderLight: 'rgba(124, 58, 237, 0.25)',
    borderMedium: 'rgba(124, 58, 237, 0.5)',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 40,
  },
  typography: {
    h1: {
      fontSize: 24,
      fontWeight: '800' as const,
      letterSpacing: 1.5,
    },
    h2: {
      fontSize: 18,
      fontWeight: '800' as const,
      letterSpacing: 2,
    },
    body: {
      fontSize: 14,
      fontWeight: '400' as const,
    },
    caption: {
      fontSize: 10,
      fontWeight: '600' as const,
      letterSpacing: 0.5,
    }
  },
  shadows: {
    neonGlow: {
      shadowColor: '#A855F7',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 1,
      shadowRadius: 20,
      elevation: 15,
    },
    panelShadow: {
      shadowColor: '#7C3AED',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.3,
      shadowRadius: 15,
      elevation: 10,
    }
  }
};
