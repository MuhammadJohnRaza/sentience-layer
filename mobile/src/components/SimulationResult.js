import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { GitBranch, AlertCircle, CheckCircle } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_MUTED = '#A7A7B5';

export function SimulationResult({ scenarioName, probability, status = 'success', branchesExplored }) {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.titleRow}>
          <GitBranch color={PRIMARY_NEON} size={16} />
          <Text style={styles.title}>{scenarioName}</Text>
        </View>
        <View style={styles.statusIcon}>
          {status === 'success' ? (
            <CheckCircle color="#32D74B" size={16} />
          ) : (
            <AlertCircle color="#FF453A" size={16} />
          )}
        </View>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>PROBABILITY</Text>
          <Text style={[styles.statValue, { color: status === 'success' ? '#32D74B' : '#FF453A' }]}>
            {(probability * 100).toFixed(1)}%
          </Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>BRANCHES</Text>
          <Text style={styles.statValue}>{branchesExplored}</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.15)',
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  title: {
    color: '#F5F5F7',
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 1,
  },
  statusIcon: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    padding: 6,
    borderRadius: 12,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statBox: {
    flex: 1,
    alignItems: 'center',
  },
  divider: {
    width: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  statLabel: {
    color: TEXT_MUTED,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
    marginBottom: 4,
  },
  statValue: {
    color: '#F5F5F7',
    fontSize: 18,
    fontWeight: '800',
    fontFamily: 'monospace',
  }
});
