import React from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const { width } = Dimensions.get('window');

const CAUSAL_NODES = [
  { id: '1', label: 'User Intent', type: 'cause', confidence: 0.98 },
  { id: '2', label: 'Market Shift', type: 'mediator', confidence: 0.74 },
  { id: '3', label: 'Kernel Action', type: 'effect', confidence: 0.92 }
];

export default function CausalScreen() {
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.title}>Causal Explorer</Text>
        <Text style={styles.subtitle}>Relational logic and intervention mapping</Text>
      </View>

      <View style={styles.graphPreview}>
        <Icon name="graph" size={120} color="#f43f5e20" />
        <Text style={styles.graphText}>Interactive Graph Active</Text>
      </View>

      <Text style={styles.sectionTitle}>Active Causal Chain</Text>
      {CAUSAL_NODES.map((node, index) => (
        <View key={node.id} style={styles.nodeCard}>
          <View style={styles.nodeIcon}>
            <Icon 
              name={node.type === 'cause' ? 'ray-start' : node.type === 'mediator' ? 'ray-vertex' : 'ray-end'} 
              size={24} 
              color="#f43f5e" 
            />
          </View>
          <View style={styles.nodeInfo}>
            <Text style={styles.nodeLabel}>{node.label}</Text>
            <Text style={styles.nodeType}>{node.type.toUpperCase()}</Text>
          </View>
          <View style={styles.confidenceContainer}>
            <Text style={styles.confidenceVal}>{Math.round(node.confidence * 100)}%</Text>
            <Text style={styles.confidenceLabel}>CONF</Text>
          </View>
        </View>
      ))}

      <View style={styles.interventionCard}>
        <Text style={styles.intTitle}>Run Intervention</Text>
        <Text style={styles.intDesc}>What happens if "Market Shift" is suppressed?</Text>
        <TouchableOpacity style={styles.intBtn}>
          <Text style={styles.intBtnText}>SIMULATE INTERVENTION</Text>
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
  graphPreview: {
    height: 200,
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#f43f5e40',
    marginBottom: 24
  },
  graphText: {
    color: '#f43f5e',
    fontSize: 12,
    fontWeight: 'bold',
    marginTop: 10,
    letterSpacing: 1
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginHorizontal: 20,
    marginBottom: 16
  },
  nodeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    padding: 16,
    borderRadius: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  nodeIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: '#f43f5e10',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16
  },
  nodeInfo: {
    flex: 1
  },
  nodeLabel: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#e0e0ff'
  },
  nodeType: {
    fontSize: 10,
    color: '#6b6b8a',
    marginTop: 2
  },
  confidenceContainer: {
    alignItems: 'flex-end'
  },
  confidenceVal: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#10b981'
  },
  confidenceLabel: {
    fontSize: 8,
    color: '#6b6b8a'
  },
  interventionCard: {
    backgroundColor: '#f43f5e10',
    marginHorizontal: 20,
    marginTop: 20,
    padding: 24,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#f43f5e30'
  },
  intTitle: {
    color: '#e0e0ff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8
  },
  intDesc: {
    color: '#6b6b8a',
    fontSize: 13,
    marginBottom: 20
  },
  intBtn: {
    backgroundColor: '#f43f5e',
    paddingVertical: 14,
    borderRadius: 14,
    alignItems: 'center'
  },
  intBtnText: {
    color: '#fff',
    fontWeight: 'bold'
  }
});
