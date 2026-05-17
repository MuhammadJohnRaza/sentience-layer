import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { User, Fingerprint } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#9B5CFF'; // Electric Violet for Mirror
const TEXT_HIGHLIGHT = '#F5F5F7';

export function MirrorScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="THE MIRROR" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <Fingerprint color={PRIMARY_NEON} size={48} style={styles.glow} />
          <Text style={styles.title}>USER COGNITIVE PROFILE</Text>
          <Text style={styles.subtitle}>Your digital reflection based on interactions.</Text>
        </View>

        <View style={styles.profileBox}>
          <View style={styles.profHeader}>
            <User color={PRIMARY_NEON} size={20} />
            <Text style={styles.profTitle}>BEHAVIORAL ALIGNMENT</Text>
          </View>
          <Text style={styles.profText}>
            The kernel observes a highly risk-averse pattern in your recent commands, favoring stability over high-variance yield operations. The Debate Agent has been weighted to challenge this bias in future interactions.
          </Text>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 40, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 18, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(155, 92, 255, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  profileBox: { backgroundColor: 'rgba(155, 92, 255, 0.05)', padding: 20, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(155, 92, 255, 0.2)' },
  profHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 16 },
  profTitle: { color: PRIMARY_NEON, fontSize: 14, fontWeight: '800', letterSpacing: 1 },
  profText: { color: '#A7A7B5', fontSize: 13, lineHeight: 22 }
});
