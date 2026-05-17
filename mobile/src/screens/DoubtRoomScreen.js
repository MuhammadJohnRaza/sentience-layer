import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { ShieldAlert, Crosshair } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#FF453A'; // Red for doubt room
const TEXT_HIGHLIGHT = '#F5F5F7';

export function DoubtRoomScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="DOUBT ROOM" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <ShieldAlert color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>ADVERSARIAL TESTING</Text>
          <Text style={styles.subtitle}>Active red-teaming and assumption challenging.</Text>
        </View>

        <View style={styles.criticismBox}>
          <View style={styles.critHeader}>
            <Crosshair color={PRIMARY_NEON} size={16} />
            <Text style={styles.critTitle}>CRITICAL WEAKNESS DETECTED</Text>
          </View>
          <Text style={styles.critText}>
            The current economic model assumes linear growth in user acquisition. The Debate Agent strongly challenges this, citing a 30% probability of market saturation within Q3.
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
  title: { color: TEXT_HIGHLIGHT, fontSize: 20, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(255, 69, 58, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  criticismBox: { backgroundColor: 'rgba(255,69,58,0.05)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(255,69,58,0.3)' },
  critHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  critTitle: { color: PRIMARY_NEON, fontSize: 12, fontWeight: '800', letterSpacing: 1 },
  critText: { color: '#A7A7B5', fontSize: 13, lineHeight: 22 }
});
