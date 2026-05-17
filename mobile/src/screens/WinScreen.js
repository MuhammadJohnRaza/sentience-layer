import React, { useEffect, useRef } from 'react';
import { StyleSheet, View, Text, Animated, Easing } from 'react-native';
import { Trophy, ArrowUpRight } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';

const PRIMARY_NEON = '#32D74B'; // Success Green
const TEXT_HIGHLIGHT = '#F5F5F7';

export function WinScreen() {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.2, duration: 1000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, easing: Easing.inOut(Easing.ease), useNativeDriver: true })
      ])
    ).start();
  }, []);

  return (
    <ScreenWrapper>
      <View style={styles.container}>
        <Animated.View style={[styles.glowRing, { transform: [{ scale: pulseAnim }] }]} />
        <View style={styles.iconContainer}>
          <Trophy color={PRIMARY_NEON} size={64} style={styles.glow} />
        </View>
        <Text style={styles.title}>OBJECTIVE ACHIEVED</Text>
        <Text style={styles.subtitle}>Multi-agent consensus reached and target executed successfully.</Text>
        
        <View style={styles.statsBox}>
          <View style={styles.statRow}>
            <Text style={styles.statLabel}>COMPUTE SAVED</Text>
            <Text style={styles.statValue}>14.2 TFLOPs</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statLabel}>YIELD INCREASE</Text>
            <View style={styles.yieldContainer}>
              <Text style={[styles.statValue, { color: PRIMARY_NEON }]}>+3.4%</Text>
              <ArrowUpRight color={PRIMARY_NEON} size={16} />
            </View>
          </View>
        </View>
      </View>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24 },
  glowRing: { position: 'absolute', width: 200, height: 200, borderRadius: 100, backgroundColor: 'rgba(50, 215, 75, 0.1)', shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 30, elevation: 10 },
  iconContainer: { marginBottom: 32 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 15 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 24, fontWeight: '900', letterSpacing: 2, marginBottom: 12, textShadowColor: 'rgba(50, 215, 75, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 14, textAlign: 'center', lineHeight: 22, marginBottom: 48 },
  statsBox: { width: '100%', backgroundColor: 'rgba(50, 215, 75, 0.05)', padding: 20, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(50, 215, 75, 0.2)' },
  statRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginVertical: 8 },
  statLabel: { color: '#A7A7B5', fontSize: 12, fontWeight: '700', letterSpacing: 1 },
  statValue: { color: TEXT_HIGHLIGHT, fontSize: 16, fontWeight: '800' },
  yieldContainer: { flexDirection: 'row', alignItems: 'center', gap: 4 }
});
