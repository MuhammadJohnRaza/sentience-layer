import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

const CAUSAL_NODES = [
  { id: '1', label: 'User Intent', type: 'cause', confidence: 0.98, icon: '🎯' },
  { id: '2', label: 'Market Shift', type: 'mediator', confidence: 0.74, icon: '📈' },
  { id: '3', label: 'Kernel Action', type: 'effect', confidence: 0.92, icon: '⚡' }
];

export default function CausalScreen() {
  const theme = useTheme();
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <ScreenWrapper>
      <TopBar
        title="CAUSAL EXPLORER"
        subtitle="🕸️ Chain-Reaction Analysis"
        showStatus={true}
      />

      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Typography variant="h1" uppercase>
            Causal Explorer
          </Typography>
          <Typography variant="body" style={styles.subtitle}>
            Relational logic and intervention mapping
          </Typography>
        </View>

        {/* Graph Visualization */}
        <Card variant="glow" style={styles.graphCard}>
          <View style={styles.graphContainer}>
            <Typography style={{ fontSize: 80, opacity: 0.1 }}>🕸️</Typography>
            <Typography variant="h3" uppercase style={styles.graphTitle}>
              Interactive Graph Active
            </Typography>
            <Typography variant="caption" style={styles.graphSubtitle}>
              Tap nodes to explore relationships
            </Typography>
          </View>
        </Card>

        {/* Active Causal Chain */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Active Causal Chain
        </Typography>

        {CAUSAL_NODES.map((node) => (
          <TouchableOpacity
            key={node.id}
            onPress={() => setSelectedNode(node)}
            activeOpacity={0.7}
          >
            <Card
              variant={selectedNode?.id === node.id ? 'elevated' : 'default'}
              style={styles.nodeCard}
            >
              <View style={[styles.nodeIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 24 }}>{node.icon}</Typography>
              </View>

              <View style={styles.nodeInfo}>
                <Typography variant="h3" uppercase style={styles.nodeLabel}>
                  {node.label}
                </Typography>
                <Typography variant="tiny" uppercase style={styles.nodeType}>
                  {node.type}
                </Typography>
              </View>

              <View style={styles.confidenceContainer}>
                <Typography variant="h2" style={[styles.confidenceVal, {
                  color: theme.colors.success
                }]}>
                  {Math.round(node.confidence * 100)}%
                </Typography>
                <Typography variant="tiny" uppercase style={styles.confidenceLabel}>
                  CONF
                </Typography>
              </View>
            </Card>
          </TouchableOpacity>
        ))}

        {/* Intervention Card */}
        <Card variant="elevated" style={styles.interventionCard}>
          <Typography variant="h2" uppercase style={styles.intTitle}>
            Run Intervention
          </Typography>
          <Typography variant="body" style={styles.intDesc}>
            What happens if "Market Shift" is suppressed?
          </Typography>
          <Button variant="primary" size="default" style={styles.intBtn}>
            <Typography variant="button" uppercase>
              SIMULATE INTERVENTION
            </Typography>
          </Button>
        </Card>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 24,
  },
  subtitle: {
    marginTop: 4,
    opacity: 0.8,
  },
  graphCard: {
    padding: 40,
    marginBottom: 24,
    minHeight: 200,
  },
  graphContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  graphTitle: {
    textAlign: 'center',
  },
  graphSubtitle: {
    textAlign: 'center',
    opacity: 0.7,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  nodeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    marginBottom: 12,
  },
  nodeIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  nodeInfo: {
    flex: 1,
    gap: 4,
  },
  nodeLabel: {
    fontSize: 14,
  },
  nodeType: {
    opacity: 0.7,
  },
  confidenceContainer: {
    alignItems: 'flex-end',
    gap: 2,
  },
  confidenceVal: {
    fontSize: 18,
  },
  confidenceLabel: {
    opacity: 0.6,
  },
  interventionCard: {
    marginTop: 20,
    padding: 24,
    gap: 16,
  },
  intTitle: {
  },
  intDesc: {
    opacity: 0.9,
  },
  intBtn: {
    marginTop: 8,
  },
});
