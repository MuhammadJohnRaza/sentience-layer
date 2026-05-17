import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { BarChart2, Zap, ArrowRight } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { MetricsCard } from '../components/MetricsCard';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function DashboardScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="EXECUTIVE DASHBOARD" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.grid}>
          <MetricsCard title="SYSTEM HEALTH" value="98%" trend="2" isPositive={true} />
          <MetricsCard title="THREAT LEVEL" value="LOW" />
        </View>

        <Text style={styles.sectionTitle}>RECENT ACTIVITY</Text>
        <View style={styles.activityBox}>
          <View style={styles.activityRow}>
            <Zap color={PRIMARY_NEON} size={14} />
            <Text style={styles.activityText}>Swarm successfully handled API spike.</Text>
          </View>
          <View style={styles.activityRow}>
            <BarChart2 color="#F6C344" size={14} />
            <Text style={styles.activityText}>Economic yield target adjusted down.</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.ctaButton}>
          <Text style={styles.ctaText}>VIEW FULL TELEMETRY</Text>
          <ArrowRight color={TEXT_HIGHLIGHT} size={16} />
        </TouchableOpacity>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  grid: { flexDirection: 'row', gap: 8, marginBottom: 24, marginTop: 10 },
  sectionTitle: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '800', letterSpacing: 2, marginBottom: 12 },
  activityBox: { backgroundColor: 'rgba(255,255,255,0.02)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(122,46,255,0.15)', marginBottom: 24 },
  activityRow: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: 'rgba(255,255,255,0.05)' },
  activityText: { color: '#A7A7B5', fontSize: 13 },
  ctaButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: PRIMARY_NEON, padding: 16, borderRadius: 16, shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 15, elevation: 8 },
  ctaText: { color: TEXT_HIGHLIGHT, fontSize: 13, fontWeight: '800', letterSpacing: 1.5 }
});
