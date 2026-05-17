import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { SimulationResult } from '../components/SimulationResult';
import { Layers } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function SimulationScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="MONTE CARLO SIMULATIONS" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <Layers color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>PREDICTIVE ENGINES</Text>
          <Text style={styles.subtitle}>Thousands of parallel futures calculated.</Text>
        </View>

        <SimulationResult scenarioName="Q3 User Acquisition Spke" probability={0.84} branchesExplored="1,048,576" status="success" />
        <SimulationResult scenarioName="Server Subsystem Failure" probability={0.12} branchesExplored="524,288" status="fail" />
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 30, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 20, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(122, 46, 255, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8, marginBottom: 20 }
});
