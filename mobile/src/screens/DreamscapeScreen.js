import React from 'react';
import { StyleSheet, View, Text, ScrollView, SafeAreaView } from 'react-native';
import { Moon, Orbit, Network } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';
const TEXT_MUTED = '#A7A7B5';

export function DreamscapeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.header}>
          <Moon color={PRIMARY_NEON} size={32} />
          <Text style={styles.title}>DREAMSCAPE CONSOLIDATION</Text>
          <Text style={styles.subtitle}>Memory formation and latent space optimization in progress.</Text>
        </View>

        <View style={styles.nodeContainer}>
          <View style={styles.pulseNode}>
            <Orbit color="#9B5CFF" size={48} />
          </View>
        </View>

        <View style={styles.logBox}>
          <View style={styles.logHeader}>
            <Network color={TEXT_MUTED} size={14} />
            <Text style={styles.logTitle}>NEURAL LOGS</Text>
          </View>
          <Text style={styles.logText}>[SYS] Consolidating memory fragments...</Text>
          <Text style={styles.logText}>[SYS] Running counterfactual simulations...</Text>
          <Text style={styles.logText}>[SYS] Pruning low-probability branches...</Text>
          <Text style={styles.logTextHighlight}>[AGENT_ALPHA] Extracted new pattern in user workflow.</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050505',
  },
  scroll: {
    padding: 24,
  },
  header: {
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 40,
  },
  title: {
    color: TEXT_HIGHLIGHT,
    fontSize: 20,
    fontWeight: '800',
    letterSpacing: 2,
    marginTop: 16,
    textShadowColor: 'rgba(122, 46, 255, 0.5)',
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 10,
  },
  subtitle: {
    color: TEXT_MUTED,
    fontSize: 12,
    textAlign: 'center',
    marginTop: 8,
    lineHeight: 18,
  },
  nodeContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 200,
    marginBottom: 40,
  },
  pulseNode: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'rgba(122, 46, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#9B5CFF',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 10,
  },
  logBox: {
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  logHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
    paddingBottom: 8,
  },
  logTitle: {
    color: TEXT_MUTED,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  logText: {
    color: TEXT_MUTED,
    fontSize: 11,
    fontFamily: 'monospace',
    marginBottom: 6,
  },
  logTextHighlight: {
    color: '#32D74B', // Success green for highlight
    fontSize: 11,
    fontFamily: 'monospace',
    marginBottom: 6,
    fontWeight: '600',
  }
});
