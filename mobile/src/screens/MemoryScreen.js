import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { BrainCircuit, Search } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#9B5CFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function MemoryScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="SHORT-TERM MEMORY" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <BrainCircuit color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>CONTEXT BUFFER</Text>
          <Text style={styles.subtitle}>Current session active working memory state.</Text>
        </View>

        <View style={styles.searchBar}>
          <Search color="#A7A7B5" size={16} />
          <Text style={styles.searchPlaceholder}>Search memory nodes...</Text>
        </View>

        <View style={styles.nodeBox}>
          <Text style={styles.nodeKey}>LAST_USER_INTENT</Text>
          <Text style={styles.nodeValue}>"Optimize server load balancing across regions"</Text>
        </View>

        <View style={styles.nodeBox}>
          <Text style={styles.nodeKey}>ACTIVE_AGENTS</Text>
          <Text style={styles.nodeValue}>[Planner, Architect, DevAgent, DebateAgent]</Text>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 30, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 18, fontWeight: '800', letterSpacing: 2, marginTop: 16 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  searchBar: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.05)', padding: 12, borderRadius: 12, marginBottom: 20, gap: 10 },
  searchPlaceholder: { color: '#A7A7B5', fontSize: 12 },
  nodeBox: { backgroundColor: 'rgba(155,92,255,0.05)', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: 'rgba(155,92,255,0.2)', marginBottom: 12, borderLeftWidth: 4, borderLeftColor: PRIMARY_NEON },
  nodeKey: { color: PRIMARY_NEON, fontSize: 10, fontWeight: '800', letterSpacing: 1, marginBottom: 6 },
  nodeValue: { color: TEXT_HIGHLIGHT, fontSize: 13, fontFamily: 'monospace' }
});
