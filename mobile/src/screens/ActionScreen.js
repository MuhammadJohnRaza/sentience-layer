import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { Zap, ShieldAlert, Cpu } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { ActionCard } from '../components/ActionCard';

const TEXT_HIGHLIGHT = '#F5F5F7';

export function ActionScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="AGENT ACTIONS" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.header}>
          <Text style={styles.title}>RECOMMENDED INTERVENTIONS</Text>
          <Text style={styles.subtitle}>The Multi-Agent Kernel requires human confirmation for the following high-level operations.</Text>
        </View>

        <View style={styles.cardGroup}>
          <ActionCard label="Deploy Server Upgrades" Icon={Cpu} onPress={() => {}} />
          <ActionCard label="Execute Market Hedge" Icon={Zap} onPress={() => {}} />
          <ActionCard label="Quarantine Sub-Network" Icon={ShieldAlert} onPress={() => {}} />
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  header: { marginBottom: 30, marginTop: 10 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 16, fontWeight: '800', letterSpacing: 1.5, marginBottom: 8 },
  subtitle: { color: '#A7A7B5', fontSize: 13, lineHeight: 20 },
  cardGroup: { gap: 12 }
});
