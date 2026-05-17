import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const { width } = Dimensions.get('window');

const MODULES = [
  { id: 'Dashboard', label: 'Dashboard', icon: 'view-dashboard', color: '#4f46e5', desc: 'System overview' },
  { id: 'Input', label: 'Comm Link', icon: 'message-text', color: '#8b5cf6', desc: 'Direct kernel input' },
  { id: 'Workflow', label: 'Trace', icon: 'map-marker-path', color: '#06b6d4', desc: 'Active workflows' },
  { id: 'Simulation', label: 'Simulate', icon: 'calculator-variant', color: '#f59e0b', desc: 'Predictive modeling' },
  { id: 'Memory', label: 'Memory', icon: 'brain', color: '#10b981', desc: 'Cognitive storage' },
  { id: 'Dreamscape', label: 'Dreamscape', icon: 'creation', color: '#ec4899', desc: 'Offline synthesis' },
  { id: 'Causal', label: 'Causal Graph', icon: 'graph', color: '#f43f5e', desc: 'Logic mapping' },
  { id: 'Economy', label: 'Economic', icon: 'chart-line', color: '#fb923c', desc: 'Value orchestration' },
  { id: 'Doubt', label: 'Doubt Room', icon: 'shield-alert', color: '#a855f7', desc: 'Confidence analysis' }
];

export default function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Sentience Layer</Text>
        <Text style={styles.subGreeting}>Welcome back, Administrator.</Text>
      </View>

      <View style={styles.statusSection}>
        <View style={styles.statusCard}>
          <Icon name="checkbox-marked-circle" size={24} color="#10b981" />
          <View>
            <Text style={styles.statusTitle}>All Systems Nominal</Text>
            <Text style={styles.statusDetail}>18 Agents | 94% Self-Awareness</Text>
          </View>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Cognitive Modules</Text>
      <View style={styles.grid}>
        {MODULES.map(module => (
          <TouchableOpacity
            key={module.id}
            style={styles.moduleCard}
            onPress={() => navigation.navigate(module.id)}
          >
            <View style={[styles.iconContainer, { backgroundColor: module.color + '20' }]}>
              <Icon name={module.icon} size={28} color={module.color} />
            </View>
            <Text style={styles.moduleLabel}>{module.label}</Text>
            <Text style={styles.moduleDesc}>{module.desc}</Text>
          </TouchableOpacity>
        ))}
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
    paddingTop: 40,
    paddingBottom: 20
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#e0e0ff',
    letterSpacing: 1
  },
  subGreeting: {
    fontSize: 14,
    color: '#6b6b8a',
    marginTop: 4
  },
  statusSection: {
    paddingHorizontal: 20,
    marginBottom: 24
  },
  statusCard: {
    backgroundColor: '#1a1a3e',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    borderWidth: 1,
    borderColor: '#10b98140'
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#e0e0ff'
  },
  statusDetail: {
    fontSize: 12,
    color: '#6b6b8a'
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginHorizontal: 20,
    marginBottom: 16
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 20,
    gap: 12
  },
  moduleCard: {
    width: (width - 52) / 2,
    backgroundColor: '#1a1a3e',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: '#2a2a4a',
    marginBottom: 12
  },
  iconContainer: {
    width: 52,
    height: 52,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12
  },
  moduleLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#e0e0ff'
  },
  moduleDesc: {
    fontSize: 11,
    color: '#6b6b8a',
    marginTop: 4
  }
});
