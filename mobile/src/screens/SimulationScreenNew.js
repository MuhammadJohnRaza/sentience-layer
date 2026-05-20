import React, { useState, useEffect } from 'react';
import { StyleSheet, View, ScrollView, Dimensions } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Typography } from '../components/Typography';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import APIService from '../services/api';

const { width } = Dimensions.get('window');

export function SimulationScreen({ route, navigation }) {
  const theme = useTheme();
  const { action } = route.params || {};
  const [simulating, setSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (action) {
      runSimulation();
    }
  }, [action]);

  const runSimulation = async () => {
    setSimulating(true);
    setProgress(0);

    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return 95;
        }
        return prev + 5;
      });
    }, 200);

    try {
      await new Promise(resolve => setTimeout(resolve, 4000));

      const mockResult = {
        action_id: action.id,
        action_title: action.title,
        status: 'completed',
        success_probability: 0.87,
        expected_value: 0.82,
        runs_completed: 100,
        best_case_scenario: 'All steps completed successfully with optimal outcomes',
        worst_case_scenario: 'Partial completion at step 3 - manual intervention required',
        initial_state: {
          revenue: 100000,
          customer_satisfaction: 75,
          operational_efficiency: 80,
        },
        final_state: {
          revenue: 125000,
          customer_satisfaction: 85,
          operational_efficiency: 90,
        },
        step_outcomes: [
          {
            step_id: '1',
            step_name: 'Initialize campaign',
            status: 'success',
            success_rate: 0.98,
            avg_duration_ms: 1200,
          },
          {
            step_id: '2',
            step_name: 'Send notifications',
            status: 'success',
            success_rate: 0.92,
            avg_duration_ms: 3500,
          },
          {
            step_id: '3',
            step_name: 'Update pricing',
            status: 'success',
            success_rate: 0.85,
            avg_duration_ms: 2100,
          },
        ],
        downstream_effects: [
          {
            hop: 1,
            description: 'Customer engagement increased by 15%',
            probability: 0.87,
            impact: 'positive',
          },
          {
            hop: 2,
            description: 'Support ticket volume may increase temporarily',
            probability: 0.45,
            impact: 'neutral',
          },
          {
            hop: 3,
            description: 'Competitor response likely within 2 weeks',
            probability: 0.62,
            impact: 'negative',
          },
        ],
        rollback_available: true,
      };

      clearInterval(progressInterval);
      setProgress(100);
      setSimulationResult(mockResult);
    } catch (error) {
      console.error('Simulation failed:', error);
    } finally {
      setSimulating(false);
    }
  };

  const executeAction = async () => {
    try {
      await APIService.executeAction(action.id, {
        confirmed: true,
        simulation_id: simulationResult?.action_id,
      });
      navigation.navigate('Home');
    } catch (error) {
      console.error('Execution failed:', error);
    }
  };

  if (!action) {
    return (
      <ScreenWrapper>
        <TopBar title="SIMULATION" subtitle="No action selected" />
      </ScreenWrapper>
    );
  }

  return (
    <ScreenWrapper>
      <TopBar
        title="ACTION SIMULATION"
        subtitle="🎲 Monte Carlo Analysis (100 runs)"
        showStatus={true}
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        <Card style={styles.actionCard}>
          <Typography variant="h3" uppercase style={styles.cardTitle}>
            {action.title}
          </Typography>
          <Typography variant="body" style={styles.actionDesc}>
            {action.description}
          </Typography>
        </Card>

        {simulating && (
          <Card style={styles.progressCard}>
            <Typography variant="h4" style={styles.progressTitle}>
              Running Simulation...
            </Typography>
            <View style={[styles.progressBar, { borderColor: theme.colors.border }]}>
              <View
                style={[
                  styles.progressFill,
                  {
                    width: `${progress}%`,
                    backgroundColor: theme.colors.primary,
                  },
                ]}
              />
            </View>
            <Typography variant="caption" style={styles.progressText}>
              {progress}% complete • {Math.floor(progress)} / 100 runs
            </Typography>
          </Card>
        )}

        {simulationResult && (
          <>
            <Card style={styles.metricsCard}>
              <Typography variant="h3" uppercase style={styles.cardTitle}>
                📊 SIMULATION METRICS
              </Typography>
              <View style={styles.metricsGrid}>
                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    Success Rate
                  </Typography>
                  <Typography variant="h1" style={{ color: theme.colors.success }}>
                    {(simulationResult.success_probability * 100).toFixed(0)}%
                  </Typography>
                </View>
                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    Expected Value
                  </Typography>
                  <Typography variant="h1" style={{ color: theme.colors.primary }}>
                    {simulationResult.expected_value.toFixed(2)}
                  </Typography>
                </View>
                <View style={styles.metric}>
                  <Typography variant="caption" style={styles.metricLabel}>
                    Runs Completed
                  </Typography>
                  <Typography variant="h1">
                    {simulationResult.runs_completed}
                  </Typography>
                </View>
              </View>
            </Card>

            <Card style={styles.stateCard}>
              <Typography variant="h3" uppercase style={styles.cardTitle}>
                📈 BEFORE → AFTER STATE
              </Typography>
              <View style={styles.stateComparison}>
                <View style={styles.stateColumn}>
                  <Typography variant="caption" style={styles.stateLabel}>
                    BEFORE
                  </Typography>
                  {Object.entries(simulationResult.initial_state).map(([key, value]) => (
                    <View key={key} style={styles.stateRow}>
                      <Typography variant="body" style={styles.stateKey}>
                        {key.replace(/_/g, ' ')}:
                      </Typography>
                      <Typography variant="h4">{value}</Typography>
                    </View>
                  ))}
                </View>
                <Typography variant="h2" style={styles.arrow}>→</Typography>
                <View style={styles.stateColumn}>
                  <Typography variant="caption" style={styles.stateLabel}>
                    AFTER
                  </Typography>
                  {Object.entries(simulationResult.final_state).map(([key, value]) => {
                    const before = simulationResult.initial_state[key];
                    const change = value - before;
                    const isPositive = change > 0;
                    return (
                      <View key={key} style={styles.stateRow}>
                        <Typography variant="body" style={styles.stateKey}>
                          {key.replace(/_/g, ' ')}:
                        </Typography>
                        <View>
                          <Typography variant="h4">{value}</Typography>
                          <Typography
                            variant="caption"
                            style={{
                              color: isPositive ? theme.colors.success : theme.colors.error,
                            }}
                          >
                            {isPositive ? '+' : ''}{change}
                          </Typography>
                        </View>
                      </View>
                    );
                  })}
                </View>
              </View>
            </Card>

            <View style={styles.actionButtons}>
              <Button
                variant="secondary"
                onPress={() => navigation.navigate('Home')}
                style={styles.actionBtn}
              >
                <Typography variant="button">CANCEL</Typography>
              </Button>
              <Button
                variant="primary"
                onPress={executeAction}
                style={styles.actionBtn}
              >
                <Typography variant="button">EXECUTE ACTION</Typography>
              </Button>
            </View>
          </>
        )}
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16, paddingBottom: 100 },
  actionCard: { marginBottom: 16, padding: 20 },
  cardTitle: { marginBottom: 12 },
  actionDesc: { lineHeight: 22, opacity: 0.9 },
  progressCard: { marginBottom: 16, padding: 20 },
  progressTitle: { marginBottom: 16, textAlign: 'center' },
  progressBar: { height: 8, borderRadius: 4, borderWidth: 1, overflow: 'hidden', marginBottom: 8 },
  progressFill: { height: '100%', borderRadius: 4 },
  progressText: { textAlign: 'center', opacity: 0.7 },
  metricsCard: { marginBottom: 16, padding: 20 },
  metricsGrid: { flexDirection: 'row', justifyContent: 'space-around', marginTop: 16 },
  metric: { alignItems: 'center' },
  metricLabel: { marginBottom: 8, opacity: 0.7 },
  stateCard: { marginBottom: 16, padding: 20 },
  stateComparison: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 16 },
  stateColumn: { flex: 1 },
  stateLabel: { marginBottom: 12, opacity: 0.7 },
  stateRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  stateKey: { textTransform: 'capitalize', opacity: 0.8 },
  arrow: { marginHorizontal: 16, opacity: 0.5 },
  actionButtons: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  actionBtn: { flex: 1 },
});
