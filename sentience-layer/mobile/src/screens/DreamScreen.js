import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, ScrollView, Animated, Dimensions } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const { width } = Dimensions.get('window');

const INSIGHTS = [
  { id: '1', title: 'Causal Link Discovered', desc: 'Correlation between User Anxiety and Economic Policy confirmed.' },
  { id: '2', title: 'Pattern Emergence', desc: 'Recursive agent communication reducing latency by 4ms.' },
  { id: '3', title: 'Creative Synthesis', desc: 'Proposed new strategy for "The Win" module.' }
];

export default function DreamScreen() {
  const pulseAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.2, duration: 3000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 0.8, duration: 3000, useNativeDriver: true })
      ])
    ).start();
  }, []);

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.title}>Dreamscape</Text>
        <Text style={styles.subtitle}>Autonomous synthesis and latent learning</Text>
      </View>

      <View style={styles.visualizerContainer}>
        <Animated.View style={[styles.glow, { transform: [{ scale: pulseAnim }] }]} />
        <View style={styles.brainContainer}>
          <Icon name="brain" size={80} color="#ec4899" />
          <Text style={styles.statusText}>SYNTHESIZING...</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Emerging Insights</Text>
      {INSIGHTS.map((insight, index) => (
        <View key={insight.id} style={styles.insightCard}>
          <View style={[styles.indexBadge, { backgroundColor: index === 0 ? '#ec489920' : '#1a1a3e' }]}>
            <Text style={[styles.indexText, { color: index === 0 ? '#ec4899' : '#6b6b8a' }]}>{index + 1}</Text>
          </View>
          <View style={styles.insightContent}>
            <Text style={styles.insightTitle}>{insight.title}</Text>
            <Text style={styles.insightDesc}>{insight.desc}</Text>
          </View>
          <Icon name="chevron-right" size={20} color="#2a2a4a" />
        </View>
      ))}

      <View style={styles.actionCard}>
        <Icon name="auto-fix" size={24} color="#e0e0ff" />
        <View style={styles.actionInfo}>
          <Text style={styles.actionTitle}>Apply Synthesis</Text>
          <Text style={styles.actionDesc}>Merge 3 new patterns into core kernel.</Text>
        </View>
        <TouchableOpacity style={styles.applyBtn}>
          <Text style={styles.applyText}>Merge</Text>
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
    marginBottom: 30
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
  visualizerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 200,
    marginBottom: 40
  },
  brainContainer: {
    alignItems: 'center',
    zIndex: 2
  },
  glow: {
    position: 'absolute',
    width: 150,
    height: 150,
    borderRadius: 75,
    backgroundColor: '#ec4899',
    opacity: 0.15,
    shadowColor: '#ec4899',
    shadowRadius: 50,
    shadowOpacity: 1,
    zIndex: 1
  },
  statusText: {
    color: '#ec4899',
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 2,
    marginTop: 12
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginHorizontal: 20,
    marginBottom: 16
  },
  insightCard: {
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
  indexBadge: {
    width: 32,
    height: 32,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16
  },
  indexText: {
    fontWeight: 'bold',
    fontSize: 14
  },
  insightContent: {
    flex: 1
  },
  insightTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#e0e0ff'
  },
  insightDesc: {
    fontSize: 12,
    color: '#6b6b8a',
    marginTop: 2
  },
  actionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ec489910',
    marginHorizontal: 20,
    marginTop: 20,
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#ec489930'
  },
  actionInfo: {
    flex: 1,
    marginLeft: 16
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#e0e0ff'
  },
  actionDesc: {
    fontSize: 12,
    color: '#6b6b8a',
    marginTop: 2
  },
  applyBtn: {
    backgroundColor: '#ec4899',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 10
  },
  applyText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 12
  }
});
