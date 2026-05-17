import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { TrendingUp, DollarSign } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { MetricsCard } from '../components/MetricsCard';

const PRIMARY_NEON = '#F6C344'; // Gold for economy
const TEXT_HIGHLIGHT = '#F5F5F7';

export function EconomicModelScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="ECONOMIC MODEL" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <DollarSign color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>RESOURCE ALLOCATION</Text>
          <Text style={styles.subtitle}>Token dynamics and compute distribution.</Text>
        </View>

        <View style={styles.metricsRow}>
          <MetricsCard title="COMPUTE STAKED" value="4,200 T" trend="150" isPositive={true} />
          <MetricsCard title="YIELD RATE" value="8.4%" trend="0.2" isPositive={true} />
        </View>

        <View style={styles.chartBox}>
          <View style={styles.chartHeader}>
            <TrendingUp color={PRIMARY_NEON} size={16} />
            <Text style={styles.chartTitle}>7-DAY FORECAST</Text>
          </View>
          <View style={styles.chartMock}>
            <Text style={styles.chartMockText}>[ Dynamic Graph Rendering ]</Text>
          </View>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 30, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 20, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(246, 195, 68, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  metricsRow: { flexDirection: 'row', gap: 8, marginBottom: 20 },
  chartBox: { backgroundColor: 'rgba(255,255,255,0.03)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(246, 195, 68, 0.2)' },
  chartHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 16 },
  chartTitle: { color: PRIMARY_NEON, fontSize: 12, fontWeight: '800', letterSpacing: 1 },
  chartMock: { height: 150, backgroundColor: 'rgba(246, 195, 68, 0.05)', borderRadius: 8, alignItems: 'center', justifyContent: 'center' },
  chartMockText: { color: 'rgba(246, 195, 68, 0.5)', fontSize: 12, letterSpacing: 1, fontWeight: '600' }
});
