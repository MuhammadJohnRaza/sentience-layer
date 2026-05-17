import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Animated, Text } from 'react-native';
import { Hexagon } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const PRIMARY_GLOW = '#9B5CFF';

export function TypingIndicator({ agentName = "KERNEL REASONING" }) {
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
      <View style={styles.avatar}>
        <Hexagon color={PRIMARY_NEON} size={12} />
      </View>
      <View style={styles.bubble}>
        <Text style={styles.agentName}>{agentName}</Text>
        <View style={styles.dots}>
          {animations.map((anim, index) => (
            <Animated.View
              key={index}
              style={[
                styles.dot,
                {
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
    paddingHorizontal: 16,
  },
  avatar: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(122, 46, 255, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 8,
  },
  bubble: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: 'rgba(122, 46, 255, 0.05)',
    borderRadius: 12,
    borderTopLeftRadius: 4,
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.15)',
  },
  agentName: {
    color: PRIMARY_NEON,
    fontSize: 9,
    fontWeight: '700',
    letterSpacing: 1,
    marginBottom: 6,
  },
  dots: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 10,
    gap: 4,
  },
  dot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: PRIMARY_GLOW,
    shadowColor: PRIMARY_GLOW,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 4,
    elevation: 2,
  }
});
