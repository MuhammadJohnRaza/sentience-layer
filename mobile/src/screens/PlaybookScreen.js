import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { BookOpen, TerminalSquare, AlertTriangle } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#F6C344'; // Gold for Playbook
const TEXT_HIGHLIGHT = '#F5F5F7';

export function PlaybookScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="THE PLAYBOOK" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <BookOpen color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>KERNEL PROCEDURES</Text>
          <Text style={styles.subtitle}>Standard Operating Procedures for multi-agent interaction.</Text>
        </View>

        <TouchableOpacity style={styles.card}>
          <View style={styles.cardHeader}>
            <TerminalSquare color={PRIMARY_NEON} size={20} />
            <Text style={styles.cardTitle}>Initialization Sequence</Text>
          </View>
          <Text style={styles.cardDesc}>Steps required to reboot the global cognitive swarm safely.</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.card}>
          <View style={styles.cardHeader}>
            <AlertTriangle color="#FF453A" size={20} />
            <Text style={[styles.cardTitle, { color: '#FF453A' }]}>Emergency Containment</Text>
          </View>
          <Text style={styles.cardDesc}>Isolate anomalous agent behaviors and quarantine subnetworks.</Text>
        </TouchableOpacity>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 40, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 18, fontWeight: '800', letterSpacing: 2, marginTop: 16 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  card: { backgroundColor: 'rgba(255,255,255,0.03)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(246,195,68,0.2)', marginBottom: 12 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 },
  cardTitle: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '700' },
  cardDesc: { color: '#A7A7B5', fontSize: 12, lineHeight: 18 }
});
