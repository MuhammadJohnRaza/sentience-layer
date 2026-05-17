import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { LayoutDashboard, Zap, Activity, Hexagon } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { MetricsCard } from '../components/MetricsCard';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function MissionControlScreen({ navigation }) {
  return (
    <ScreenWrapper>
      <TopBar title="MISSION CONTROL" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.metricsRow}>
          <MetricsCard title="KERNEL UPTIME" value="99.9%" trend="0.1" isPositive={true} />
          <MetricsCard title="ACTIVE AGENTS" value="18" />
        </View>
        <View style={styles.metricsRow}>
          <MetricsCard title="LATENT THREADS" value="1,042" trend="124" isPositive={true} />
          <MetricsCard title="SYSTEM LOAD" value="42%" trend="5" isPositive={false} />
        </View>

        <Text style={styles.sectionTitle}>ACTIVE DIRECTIVES</Text>
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Zap color={PRIMARY_NEON} size={20} />
            <Text style={styles.cardTitle}>Global Optimization Protocol</Text>
          </View>
          <Text style={styles.cardDesc}>
            Running widespread causal inference over sub-agent outputs to maximize economic efficiency and minimize entropy.
          </Text>
          <View style={styles.progressTrack}>
            <View style={[styles.progressBar, { width: '74%' }]} />
          </View>
          <Text style={styles.progressText}>74% COMPLETE</Text>
        </View>

        <TouchableOpacity style={styles.bigButton}>
          <Hexagon color={TEXT_HIGHLIGHT} size={24} />
          <Text style={styles.bigButtonText}>INITIALIZE NEW DIRECTIVE</Text>
        </TouchableOpacity>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16, paddingBottom: 40 },
  metricsRow: { flexDirection: 'row', gap: 8, marginBottom: 12 },
  sectionTitle: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '700', letterSpacing: 2, marginTop: 24, marginBottom: 12 },
  card: { backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: 'rgba(122,46,255,0.2)', marginBottom: 16 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  cardTitle: { color: TEXT_HIGHLIGHT, fontSize: 16, fontWeight: '700' },
  cardDesc: { color: '#A7A7B5', fontSize: 12, lineHeight: 18, marginBottom: 16 },
  progressTrack: { height: 4, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 2, marginBottom: 8, overflow: 'hidden' },
  progressBar: { height: '100%', backgroundColor: PRIMARY_NEON, shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 5 },
  progressText: { color: '#A7A7B5', fontSize: 10, fontWeight: '600', letterSpacing: 1, textAlign: 'right' },
  bigButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 12, backgroundColor: 'rgba(122,46,255,0.15)', paddingVertical: 16, borderRadius: 16, borderWidth: 1, borderColor: PRIMARY_NEON, marginTop: 12, shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.3, shadowRadius: 10 },
  bigButtonText: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '800', letterSpacing: 1.5 }
});
