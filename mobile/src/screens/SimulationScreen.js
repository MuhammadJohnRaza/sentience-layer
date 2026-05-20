import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function SimulationScreen() {
  const theme = useTheme();

  const simulations = [
    {
      id: 1,
      name: 'Q3 User Acquisition Spike',
      probability: 0.84,
      branches: '1,048,576',
      status: 'success',
      confidence: 'high',
    },
    {
      id: 2,
      name: 'Server Subsystem Failure',
      probability: 0.12,
      branches: '524,288',
      status: 'warning',
      confidence: 'medium',
    },
    {
      id: 3,
      name: 'Market Volatility Impact',
      probability: 0.67,
      branches: '2,097,152',
      status: 'success',
      confidence: 'high',
    },
  ];

  return (
    <ScreenWrapper>
      <TopBar
        title="MONTE CARLO SIMULATIONS"
        subtitle="🎯 Predictive Engines"
        showStatus={true}
      />

      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Header */}
        <View style={styles.header}>
          <View style={[styles.headerIcon, {
            backgroundColor: 'rgba(124, 58, 237, 0.2)',
            borderColor: theme.colors.borderMedium,
            ...theme.shadows.neonGlow,
          }]}>
            <Typography style={{ fontSize: 40 }}>🎯</Typography>
          </View>

          <Typography variant="h1" uppercase style={styles.headerTitle}>
            Predictive Engines
          </Typography>

          <Typography variant="body" style={styles.headerSubtitle}>
            Thousands of parallel futures calculated
          </Typography>
        </View>

        {/* Simulations List */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Active Simulations
        </Typography>

        {simulations.map((sim) => (
          <TouchableOpacity key={sim.id} activeOpacity={0.7}>
            <Card variant="elevated" style={styles.simCard}>
              <View style={styles.simHeader}>
                <Typography variant="h3" uppercase style={styles.simName}>
                  {sim.name}
                </Typography>
                <View style={[styles.statusBadge, {
                  backgroundColor: sim.status === 'success' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(252, 211, 77, 0.2)',
                  borderColor: sim.status === 'success' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(252, 211, 77, 0.3)',
                }]}>
                  <Typography variant="tiny" uppercase style={{
                    color: sim.status === 'success' ? theme.colors.success : theme.colors.accentGold
                  }}>
                    {sim.status}
                  </Typography>
                </View>
              </View>

              <View style={styles.simMetrics}>
                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    PROBABILITY
                  </Typography>
                  <Typography variant="h2" style={[styles.metricValue, {
                    color: sim.probability > 0.7 ? theme.colors.success :
                           sim.probability > 0.4 ? theme.colors.accentGold :
                           theme.colors.danger
                  }]}>
                    {Math.round(sim.probability * 100)}%
                  </Typography>
                </View>

                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    BRANCHES
                  </Typography>
                  <Typography variant="h3" style={styles.metricValue}>
                    {sim.branches}
                  </Typography>
                </View>

                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    CONFIDENCE
                  </Typography>
                  <Typography variant="bodyBold" uppercase style={styles.metricValue}>
                    {sim.confidence}
                  </Typography>
                </View>
              </View>
            </Card>
          </TouchableOpacity>
        ))}

        {/* Actions */}
        <View style={styles.actions}>
          <Button variant="primary" size="lg" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              RUN NEW SIMULATION
            </Typography>
          </Button>
          <Button variant="outline" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              VIEW HISTORY
            </Typography>
          </Button>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: {
    padding: 16,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    paddingVertical: 32,
    gap: 12,
    marginBottom: 24,
  },
  headerIcon: {
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  headerTitle: {
    textAlign: 'center',
  },
  headerSubtitle: {
    textAlign: 'center',
    opacity: 0.8,
    paddingHorizontal: 32,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  simCard: {
    padding: 20,
    marginBottom: 16,
    gap: 16,
  },
  simHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  simName: {
    flex: 1,
    fontSize: 14,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
  },
  simMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(124, 58, 237, 0.2)',
  },
  metric: {
    flex: 1,
    alignItems: 'center',
    gap: 6,
  },
  metricLabel: {
    opacity: 0.7,
  },
  metricValue: {
    textAlign: 'center',
  },
  actions: {
    gap: 12,
    marginTop: 24,
  },
  actionBtn: {
    width: '100%',
  },
});
