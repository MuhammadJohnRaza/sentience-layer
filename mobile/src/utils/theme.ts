export const theme = {
  colors: {
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
      shadowColor: '#9B5CFF',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 1,
      shadowRadius: 20,
      elevation: 15,
    },
    panelShadow: {
      shadowColor: '#7A2EFF',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.3,
      shadowRadius: 15,
      elevation: 10,
    }
  }
};
