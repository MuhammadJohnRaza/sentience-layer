import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Animated } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

export function TypingIndicator({ agentName = 'COGNITIVE KERNEL' }) {
  const theme = useTheme();
  const [animations] = useState([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]);

  useEffect(() => {
    const createAnimation = (anim, delay) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(anim, {
            toValue: 1,
            duration: 600,
            useNativeDriver: true,
          }),
          Animated.timing(anim, {
            toValue: 0,
            duration: 600,
            useNativeDriver: true,
          })
        ])
      );
    };

    const anims = animations.map((anim, i) => createAnimation(anim, i * 200));
    Animated.parallel(anims).start();

    return () => anims.forEach(a => a.stop());
  }, [animations]);

  return (
    <View style={styles.container}>
      {/* Avatar */}
      <View style={[styles.avatar, {
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
        borderColor: 'rgba(245, 158, 11, 0.3)',
        borderWidth: 2,
        shadowColor: '#F59E0B',
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.25,
        shadowRadius: 12,
        elevation: 5,
      }]}>
        <Typography style={{ fontSize: 16 }}>🧠</Typography>
      </View>

      {/* Bubble */}
      <View style={[styles.bubble, {
        backgroundColor: theme.colors.card,
        borderColor: 'rgba(124, 58, 237, 0.2)',
        borderWidth: 1,
        shadowColor: '#000000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.6,
        shadowRadius: 15,
        elevation: 8,
      }]}>
        <Typography variant="tiny" uppercase style={[styles.agentName, {
          color: '#FCD34D'
        }]}>
          {agentName}
        </Typography>
        <View style={styles.dots}>
          {animations.map((anim, index) => (
            <Animated.View
              key={index}
              style={[
                styles.dot,
                {
                  backgroundColor: theme.colors.primaryGlow,
                  shadowColor: theme.colors.primaryGlow,
                  opacity: anim.interpolate({ inputRange: [0, 1], outputRange: [0.3, 1] }),
                  transform: [
                    {
                      translateY: anim.interpolate({ inputRange: [0, 1], outputRange: [0, -4] })
                    }
                  ]
                }
              ]}
            />
          ))}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
    maxWidth: '85%',
    gap: 12,
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
  },
  bubble: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 16,
    borderTopLeftRadius: 4,
  },
  agentName: {
    marginBottom: 8,
  },
  dots: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 12,
    gap: 6,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 6,
    elevation: 3,
  }
});
