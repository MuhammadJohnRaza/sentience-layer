import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { Activity, Radio } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function TraceScreen() {
  const logs = [
    { time: '14:02:44', event: 'Initiated Agent Swarm Alpha' },
    { time: '14:02:48', event: 'Evaluating branch probabilities' },
    { time: '14:03:12', event: 'Debate Agent challenged hypothesis' },
    { time: '14:04:05', event: 'Consensus Reached. Proceeding.' }
  ];

  return (
    <ScreenWrapper>
      <TopBar title="EXECUTION TRACE" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.header}>
          <Radio color={PRIMARY_NEON} size={24} style={styles.glow} />
          <Text style={styles.title}>LIVE TELEMETRY</Text>
        </View>

        <View style={styles.logBox}>
          {logs.map((log, index) => (
            <View key={index} style={styles.logRow}>
              <Text style={styles.timeText}>[{log.time}]</Text>
              <Text style={styles.eventText}>{log.event}</Text>
            </View>
          ))}
          <View style={styles.activeRow}>
            <Activity color={PRIMARY_NEON} size={14} />
            <Text style={styles.activeText}>Awaiting further kernel input...</Text>
          </View>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  header: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 24, marginTop: 10 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 10 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 16, fontWeight: '800', letterSpacing: 2 },
  logBox: { backgroundColor: 'rgba(11, 11, 18, 0.8)', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: 'rgba(122, 46, 255, 0.15)' },
  logRow: { flexDirection: 'row', marginBottom: 12 },
  timeText: { color: PRIMARY_NEON, fontSize: 11, fontFamily: 'monospace', marginRight: 12, opacity: 0.8 },
  eventText: { color: '#A7A7B5', fontSize: 12, flex: 1, lineHeight: 18 },
  activeRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 16, paddingTop: 16, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)' },
  activeText: { color: PRIMARY_NEON, fontSize: 11, fontFamily: 'monospace', fontStyle: 'italic' }
});
