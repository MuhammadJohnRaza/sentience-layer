export const theme = {
  colors: {
    // Backgrounds
    backgroundPrimary: '#000000',
    backgroundSecondary: '#111111',
    card: '#111111',
    surface: '#111111',

    // Primary Purple
    primaryNeon: '#7C3AED',
    primaryGlow: '#A855F7',
    primary: '#7C3AED',

    // Gold/Yellow Accents
    accentGold: '#FCD34D',
    textHighlight: '#FCD34D',

    // Text Colors
    textBody: '#FDE68A',
    textMuted: '#D4D4D8',
    foreground: '#FDE68A',

    // Status Colors
    danger: '#EF4444',
    destructive: '#EF4444',
    success: '#22C55E',
    emerald: '#10B981',

    // Borders
    borderLight: 'rgba(124, 58, 237, 0.25)',
    borderMedium: 'rgba(124, 58, 237, 0.5)',
    border: 'rgba(124, 58, 237, 0.25)',
    borderHover: 'rgba(124, 58, 237, 0.5)',

    // Transparent overlays
    cardOverlay: 'rgba(17, 17, 17, 0.6)',
    backgroundOverlay: 'rgba(0, 0, 0, 0.4)',
    primaryOverlay: 'rgba(124, 58, 237, 0.1)',
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
      fontSize: 28,
      fontWeight: '800',
      letterSpacing: 2,
    },
    h2: {
      fontSize: 20,
      fontWeight: '800',
      letterSpacing: 2,
    },
    h3: {
      fontSize: 16,
      fontWeight: '700',
      letterSpacing: 1.5,
    },
    body: {
      fontSize: 14,
      fontWeight: '500',
      letterSpacing: 0.5,
    },
    bodyBold: {
      fontSize: 14,
      fontWeight: '700',
      letterSpacing: 0.8,
    },
    caption: {
      fontSize: 11,
      fontWeight: '700',
      letterSpacing: 1,
    },
    tiny: {
      fontSize: 9,
      fontWeight: '800',
      letterSpacing: 1.5,
    },
    button: {
      fontSize: 12,
      fontWeight: '800',
      letterSpacing: 1.5,
    }
  },
  borderRadius: {
    sm: 8,
    md: 12,
    lg: 16,
    xl: 20,
    full: 9999,
  },
  shadows: {
    neonGlow: {
      shadowColor: '#A855F7',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.8,
      shadowRadius: 20,
      elevation: 15,
    },
    panelShadow: {
      shadowColor: '#000000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.8,
      shadowRadius: 25,
      elevation: 10,
    },
    cardShadow: {
      shadowColor: '#000000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.5,
      shadowRadius: 15,
      elevation: 8,
    },
    buttonGlow: {
      shadowColor: '#7C3AED',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.6,
      shadowRadius: 15,
      elevation: 8,
    }
  }
};
