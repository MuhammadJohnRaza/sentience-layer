import { Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

export const CONSTANTS = {
  // Application
  APP_NAME: 'Sentience Layer',
  APP_VERSION: '3.1.4',
  
  // Storage Keys
  STORAGE_KEYS: {
    USER_PREFS: '@sentience_user_prefs',
    AUTH_TOKEN: '@sentience_auth_token',
    OFFLINE_QUEUE: 'SENTIENCE_OFFLINE_QUEUE',
    THEME_MODE: '@sentience_theme',
  },

  // Dimensions
  SCREEN_WIDTH: width,
  SCREEN_HEIGHT: height,
  IS_IOS: Platform.OS === 'ios',
  IS_ANDROID: Platform.OS === 'android',

  // Animation Timing
  ANIMATION: {
    FAST: 200,
    NORMAL: 350,
    SLOW: 600,
    PULSE: 1200,
  },

  // Agent Status Constants
  AGENT_STATUS: {
    IDLE: 'IDLE',
    REASONING: 'REASONING',
    EXECUTING: 'EXECUTING',
    ERROR: 'ERROR',
    SLEEP: 'SLEEP'
  }
};
