import React from 'react';
import { StyleSheet, View, ScrollView } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function DreamscapeScreen() {
  const theme = useTheme();

  const neuralLogs = [
    { id: 1, type: 'SYS', message: 'Consolidating memory fragments...', status: 'processing' },
    { id: 2, type: 'SYS', message: 'Running counterfactual simulations...', status: 'processing' },
    { id: 3, type: 'SYS', message: 'Pruning low-probability branches...', status: 'processing' },
    { id: 4, type: 'AGENT_ALPHA', message: 'Extracted new pattern in user workflow.', status: 'success' },
  ];

  return (
    <ScreenWrapper>
      <TopBar
        title="DREAMSCAPE"
        subtitle="🌌 Memory Consolidation"
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
            <Typography style={{ fontSize: 40 }}>🌌</Typography>
          </View>

          <Typography variant="h1" uppercase style={styles.headerTitle}>
            Dreamscape Consolidation
          </Typography>

          <Typography variant="body" style={styles.headerSubtitle}>
            Memory formation and latent space optimization in progress
          </Typography>
        </View>

        {/* Pulse Node Visualization */}
        <Card variant="glow" style={styles.visualCard}>
          <View style={styles.pulseContainer}>
            <View style={[styles.pulseNode, {
              backgroundColor: 'rgba(124, 58, 237, 0.15)',
              borderColor: theme.colors.borderMedium,
              shadowColor: theme.colors.primaryGlow,
              shadowOffset: { width: 0, height: 0 },
              shadowOpacity: 0.5,
              shadowRadius: 20,
              elevation: 10,
            }]}>
              <Typography style={{ fontSize: 48 }}>🧠</Typography>
            </View>
            <Typography variant="caption" style={styles.pulseLabel}>
              NEURAL CONSOLIDATION ACTIVE
            </Typography>
          </View>
        </Card>

        {/* Neural Logs */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Neural Logs
        </Typography>

        <Card variant="default" style={styles.logCard}>
          <View style={styles.logHeader}>
            <Typography style={{ fontSize: 14 }}>🔗</Typography>
            <Typography variant="tiny" uppercase style={styles.logTitle}>
              System Activity
            </Typography>
          </View>

          {neuralLogs.map((log) => (
            <View key={log.id} style={styles.logRow}>
              <Typography variant="caption" style={[styles.logType, {
                color: log.status === 'success' ? theme.colors.success : theme.colors.primaryNeon
              }]}>
                [{log.type}]
              </Typography>
              <Typography variant="body" style={[styles.logMessage, {
                color: log.status === 'success' ? theme.colors.success : theme.colors.textBody
              }]}>
                {log.message}
              </Typography>
            </View>
          ))}
        </Card>

        {/* Actions */}
        <View style={styles.actions}>
          <Button variant="primary" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              FORCE CONSOLIDATION
            </Typography>
          </Button>
          <Button variant="outline" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              VIEW DREAM LOG
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
    lineHeight: 22,
  },
  visualCard: {
    padding: 40,
    marginBottom: 24,
    minHeight: 200,
  },
  pulseContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: 20,
  },
  pulseNode: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pulseLabel: {
    textAlign: 'center',
    opacity: 0.8,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  logCard: {
    padding: 16,
    marginBottom: 24,
  },
  logHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingBottom: 12,
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(124, 58, 237, 0.2)',
  },
  logTitle: {
    opacity: 0.7,
  },
  logRow: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 8,
  },
  logType: {
    fontFamily: 'monospace',
    fontWeight: '800',
  },
  logMessage: {
    flex: 1,
    fontFamily: 'monospace',
    fontSize: 12,
  },
  actions: {
    gap: 12,
  },
  actionBtn: {
    width: '100%',
  },
});
