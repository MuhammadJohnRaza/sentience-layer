import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { LineChart } from 'react-native-chart-kit';

const { width } = Dimensions.get('window');

const CONFLICTS = [
  { id: '1', agentA: 'Memory', agentB: 'Causal', topic: 'Temporal Sequence', entropy: 0.82 },
  { id: '2', agentA: 'Economic', agentB: 'Strategy', topic: 'Budget Allocation', entropy: 0.45 },
  { id: '3', agentA: 'Dream', agentB: 'Kernel', topic: 'Pattern Validity', entropy: 0.12 }
];

export default function DoubtScreen() {
  const [activeConflict, setActiveConflict] = useState(CONFLICTS[0]);

  const chartConfig = {
    backgroundGradientFrom: '#1a1a3e',
    backgroundGradientTo: '#1a1a3e',
    color: (opacity = 1) => `rgba(168, 85, 247, ${opacity})`,
    strokeWidth: 2
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.title}>Doubt Room</Text>
        <Text style={styles.subtitle}>Conflict resolution and entropy tracking</Text>
      </View>

      <View style={styles.entropyCard}>
        <View style={styles.cardHeader}>
          <Icon name="chart-bell-curve" size={20} color="#a855f7" />
          <Text style={styles.cardTitle}>Global Entropy</Text>
        </View>
        <LineChart
          data={{
            labels: ['1h', '45m', '30m', '15m', 'Now'],
            datasets: [{ data: [0.1, 0.4, 0.3, 0.8, 0.6] }]
          }}
          width={width - 72}
          height={160}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </View>

      <Text style={styles.sectionTitle}>Agent Conflicts (The Theater)</Text>
      {CONFLICTS.map(conflict => (
        <TouchableOpacity 
          key={conflict.id} 
          style={[styles.conflictCard, activeConflict.id === conflict.id && styles.activeConflict]}
          onPress={() => setActiveConflict(conflict)}
        >
          <View style={styles.conflictHeader}>
            <View style={styles.agents}>
              <View style={styles.agentBadge}><Text style={styles.agentText}>{conflict.agentA}</Text></View>
              <Icon name="sword-cross" size={16} color="#6b6b8a" />
              <View style={styles.agentBadge}><Text style={styles.agentText}>{conflict.agentB}</Text></View>
            </View>
            <View style={[styles.entropyBadge, { backgroundColor: conflict.entropy > 0.6 ? '#ef444420' : '#f59e0b20' }]}>
              <Text style={[styles.entropyText, { color: conflict.entropy > 0.6 ? '#ef4444' : '#f59e0b' }]}>
                {Math.round(conflict.entropy * 100)}% Doubt
              </Text>
            </View>
          </View>
          <Text style={styles.topicText}>Subject: {conflict.topic}</Text>
        </TouchableOpacity>
      ))}

      <View style={styles.resolutionPanel}>
        <Text style={styles.resolutionTitle}>Mediation Active</Text>
        <Text style={styles.resolutionDesc}>Kernel is currently observing the dialectic between {activeConflict.agentA} and {activeConflict.agentB}.</Text>
        <TouchableOpacity style={styles.resolveBtn}>
          <Text style={styles.resolveBtnText}>FORCE CONSENSUS</Text>
        </TouchableOpacity>
      </View>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a1a'
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    marginBottom: 24
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#e0e0ff'
  },
  subtitle: {
    fontSize: 14,
    color: '#6b6b8a',
    marginTop: 4
  },
  entropyCard: {
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
    borderColor: '#a855f740',
    marginBottom: 24
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16
  },
  cardTitle: {
    color: '#e0e0ff',
    fontWeight: 'bold',
    fontSize: 14
  },
  chart: {
    marginLeft: -10,
    borderRadius: 12
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginHorizontal: 20,
    marginBottom: 16
  },
  conflictCard: {
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  activeConflict: {
    borderColor: '#a855f7',
    backgroundColor: '#a855f705'
  },
  conflictHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10
  },
  agents: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8
  },
  agentBadge: {
    backgroundColor: '#0f0f23',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  agentText: {
    color: '#94a3b8',
    fontSize: 11,
    fontWeight: 'bold'
  },
  entropyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12
  },
  entropyText: {
    fontSize: 10,
    fontWeight: 'bold'
  },
  topicText: {
    color: '#e0e0ff',
    fontSize: 14,
    fontWeight: '500'
  },
  resolutionPanel: {
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    marginTop: 20,
    padding: 24,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#2a2a4a',
    alignItems: 'center'
  },
  resolutionTitle: {
    color: '#e0e0ff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8
  },
  resolutionDesc: {
    color: '#6b6b8a',
    fontSize: 13,
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 20
  },
  resolveBtn: {
    backgroundColor: '#a855f7',
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 14,
    width: '100%',
    alignItems: 'center'
  },
  resolveBtnText: {
    color: '#fff',
    fontWeight: 'bold',
    letterSpacing: 1
  }
});
