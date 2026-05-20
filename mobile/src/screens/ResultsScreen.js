import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Typography } from '../components/Typography';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';

export function ResultsScreen({ route, navigation }) {
  const theme = useTheme();
  const { data } = route.params || {};
  const [expandedSection, setExpandedSection] = useState('insights');

  if (!data) {
    return (
      <ScreenWrapper>
        <TopBar title="RESULTS" subtitle="No data available" />
        <View style={styles.emptyState}>
          <Typography variant="h3">No Results</Typography>
          <Button onPress={() => navigation.goBack()}>
            <Typography>Go Back</Typography>
          </Button>
        </View>
      </ScreenWrapper>
    );
  }

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <ScreenWrapper>
      <TopBar
        title="ANALYSIS RESULTS"
        subtitle={`✓ ${data.confidence ? (data.confidence * 100).toFixed(0) : 0}% Confidence`}
        showStatus={true}
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        {/* Summary Card */}
        <Card style={styles.summaryCard}>
          <Typography variant="h3" uppercase style={styles.cardTitle}>
            📊 EXECUTIVE SUMMARY
          </Typography>
          <Typography variant="body" style={styles.summaryText}>
            {data.final_recommendation?.summary || 'Analysis completed successfully'}
          </Typography>
          <View style={styles.statsRow}>
            <View style={styles.stat}>
              <Typography variant="caption" style={styles.statLabel}>INSIGHTS</Typography>
              <Typography variant="h2" style={styles.statValue}>
                {data.insights?.length || 0}
              </Typography>
            </View>
            <View style={styles.stat}>
              <Typography variant="caption" style={styles.statLabel}>ACTIONS</Typography>
              <Typography variant="h2" style={styles.statValue}>
                {data.suggested_actions?.length || 0}
              </Typography>
            </View>
            <View style={styles.stat}>
              <Typography variant="caption" style={styles.statLabel}>TIME</Typography>
              <Typography variant="h2" style={styles.statValue}>
                {data.execution_time_ms ? `${(data.execution_time_ms / 1000).toFixed(1)}s` : 'N/A'}
              </Typography>
            </View>
          </View>
        </Card>

        {/* Understanding Section */}
        <TouchableOpacity onPress={() => toggleSection('understanding')}>
          <Card style={styles.sectionCard}>
            <View style={styles.sectionHeader}>
              <Typography variant="h3" uppercase>
                🧠 CONTENT UNDERSTANDING
              </Typography>
              <Typography style={styles.expandIcon}>
                {expandedSection === 'understanding' ? '▼' : '▶'}
              </Typography>
            </View>
            {expandedSection === 'understanding' && data.understanding && (
              <View style={styles.sectionContent}>
                <View style={styles.infoRow}>
                  <Typography variant="caption" style={styles.label}>Intent:</Typography>
                  <Typography variant="body">{data.understanding.intent || 'N/A'}</Typography>
                </View>
                <View style={styles.infoRow}>
                  <Typography variant="caption" style={styles.label}>Urgency:</Typography>
                  <Typography variant="body">
                    {data.understanding.urgency_score ? `${(data.understanding.urgency_score * 100).toFixed(0)}%` : 'N/A'}
                  </Typography>
                </View>
                <View style={styles.infoRow}>
                  <Typography variant="caption" style={styles.label}>Summary:</Typography>
                  <Typography variant="body">{data.understanding.summary || 'N/A'}</Typography>
                </View>
                {data.understanding.topics && data.understanding.topics.length > 0 && (
                  <View style={styles.tagsContainer}>
                    {data.understanding.topics.map((topic, idx) => (
                      <View key={idx} style={[styles.tag, { borderColor: theme.colors.border }]}>
                        <Typography variant="caption">{topic}</Typography>
                      </View>
                    ))}
                  </View>
                )}
              </View>
            )}
          </Card>
        </TouchableOpacity>

        {/* Insights Section */}
        <TouchableOpacity onPress={() => toggleSection('insights')}>
          <Card style={styles.sectionCard}>
            <View style={styles.sectionHeader}>
              <Typography variant="h3" uppercase>
                💡 KEY INSIGHTS
              </Typography>
              <Typography style={styles.expandIcon}>
                {expandedSection === 'insights' ? '▼' : '▶'}
              </Typography>
            </View>
            {expandedSection === 'insights' && data.insights && (
              <View style={styles.sectionContent}>
                {data.insights.map((insight, idx) => (
                  <View key={idx} style={[styles.insightCard, { borderColor: theme.colors.border }]}>
                    <View style={styles.insightHeader}>
                      <Typography variant="body" style={styles.insightType}>
                        {insight.type?.toUpperCase() || 'INSIGHT'}
                      </Typography>
                      <Typography variant="caption" style={styles.confidence}>
                        {insight.confidence ? `${(insight.confidence * 100).toFixed(0)}%` : 'N/A'}
                      </Typography>
                    </View>
                    <Typography variant="h4" style={styles.insightTitle}>
                      {insight.title}
                    </Typography>
                    <Typography variant="body" style={styles.insightDesc}>
                      {insight.description}
                    </Typography>
                    {insight.severity && (
                      <View style={[styles.severityBadge, {
                        backgroundColor: insight.severity === 'high' ? 'rgba(239, 68, 68, 0.2)' :
                                       insight.severity === 'medium' ? 'rgba(251, 191, 36, 0.2)' :
                                       'rgba(34, 197, 94, 0.2)'
                      }]}>
                        <Typography variant="caption">{insight.severity.toUpperCase()}</Typography>
                      </View>
                    )}
                  </View>
                ))}
              </View>
            )}
          </Card>
        </TouchableOpacity>

        {/* Reasoning Chain Section */}
        <TouchableOpacity onPress={() => toggleSection('reasoning')}>
          <Card style={styles.sectionCard}>
            <View style={styles.sectionHeader}>
              <Typography variant="h3" uppercase>
                🔗 REASONING CHAIN
              </Typography>
              <Typography style={styles.expandIcon}>
                {expandedSection === 'reasoning' ? '▼' : '▶'}
              </Typography>
            </View>
            {expandedSection === 'reasoning' && data.reasoning_chain && (
              <View style={styles.sectionContent}>
                {data.reasoning_chain.map((step, idx) => (
                  <View key={idx} style={[styles.reasoningStep, { borderColor: theme.colors.border }]}>
                    <Typography variant="caption" style={styles.stepNumber}>
                      STEP {step.step}
                    </Typography>
                    <Typography variant="body" style={styles.stepThought}>
                      💭 {step.thought}
                    </Typography>
                    <Typography variant="body" style={styles.stepAction}>
                      ⚡ Action: {step.action}
                    </Typography>
                    <Typography variant="body" style={styles.stepObservation}>
                      👁️ {step.observation}
                    </Typography>
                  </View>
                ))}
              </View>
            )}
          </Card>
        </TouchableOpacity>

        {/* Actions Section */}
        <TouchableOpacity onPress={() => toggleSection('actions')}>
          <Card style={styles.sectionCard}>
            <View style={styles.sectionHeader}>
              <Typography variant="h3" uppercase>
                🎯 RECOMMENDED ACTIONS
              </Typography>
              <Typography style={styles.expandIcon}>
                {expandedSection === 'actions' ? '▼' : '▶'}
              </Typography>
            </View>
            {expandedSection === 'actions' && data.suggested_actions && (
              <View style={styles.sectionContent}>
                {data.suggested_actions.map((action, idx) => (
                  <View key={idx} style={[styles.actionCard, { borderColor: theme.colors.border }]}>
                    <Typography variant="h4" style={styles.actionTitle}>
                      {action.title}
                    </Typography>
                    <Typography variant="body" style={styles.actionDesc}>
                      {action.description}
                    </Typography>
                    <View style={styles.actionFooter}>
                      <Typography variant="caption">
                        {action.steps} steps • {(action.confidence * 100).toFixed(0)}% confidence
                      </Typography>
                      <Button
                        variant="primary"
                        size="small"
                        onPress={() => navigation.navigate('Simulation', { action })}
                      >
                        <Typography variant="caption">SIMULATE</Typography>
                      </Button>
                    </View>
                  </View>
                ))}
              </View>
            )}
          </Card>
        </TouchableOpacity>

        {/* Simulations Section */}
        {data.simulations && data.simulations.length > 0 && (
          <TouchableOpacity onPress={() => toggleSection('simulations')}>
            <Card style={styles.sectionCard}>
              <View style={styles.sectionHeader}>
                <Typography variant="h3" uppercase>
                  🎲 SIMULATION RESULTS
                </Typography>
                <Typography style={styles.expandIcon}>
                  {expandedSection === 'simulations' ? '▼' : '▶'}
                </Typography>
              </View>
              {expandedSection === 'simulations' && (
                <View style={styles.sectionContent}>
                  {data.simulations.map((sim, idx) => (
                    <View key={idx} style={[styles.simCard, { borderColor: theme.colors.border }]}>
                      <Typography variant="h4" style={styles.simTitle}>
                        {sim.action_title}
                      </Typography>
                      <View style={styles.simStats}>
                        <View style={styles.simStat}>
                          <Typography variant="caption">Success Rate</Typography>
                          <Typography variant="h3" style={{ color: theme.colors.success }}>
                            {(sim.success_probability * 100).toFixed(0)}%
                          </Typography>
                        </View>
                        <View style={styles.simStat}>
                          <Typography variant="caption">Expected Value</Typography>
                          <Typography variant="h3">
                            {sim.expected_value.toFixed(2)}
                          </Typography>
                        </View>
                      </View>
                      <View style={styles.scenarios}>
                        <Typography variant="caption" style={styles.scenarioLabel}>
                          ✅ Best Case:
                        </Typography>
                        <Typography variant="body">{sim.best_case}</Typography>
                        <Typography variant="caption" style={[styles.scenarioLabel, { marginTop: 8 }]}>
                          ⚠️ Worst Case:
                        </Typography>
                        <Typography variant="body">{sim.worst_case}</Typography>
                      </View>
                    </View>
                  ))}
                </View>
              )}
            </Card>
          </TouchableOpacity>
        )}

        {/* Impact Analysis */}
        {data.impact_analysis && Object.keys(data.impact_analysis).length > 0 && (
          <Card style={styles.sectionCard}>
            <Typography variant="h3" uppercase style={styles.cardTitle}>
              📈 IMPACT ANALYSIS
            </Typography>
            <View style={styles.impactGrid}>
              <View style={styles.impactItem}>
                <Typography variant="caption">Total Impact</Typography>
                <Typography variant="h3">
                  {data.impact_analysis.total_impact_score?.toFixed(2) || 'N/A'}
                </Typography>
              </View>
              <View style={styles.impactItem}>
                <Typography variant="caption">Risk Adjusted</Typography>
                <Typography variant="h3">
                  {data.impact_analysis.risk_adjusted_score?.toFixed(2) || 'N/A'}
                </Typography>
              </View>
              <View style={styles.impactItem}>
                <Typography variant="caption">Affected Nodes</Typography>
                <Typography variant="h3">
                  {data.impact_analysis.affected_nodes || 0}
                </Typography>
              </View>
            </View>
          </Card>
        )}

        {/* Metadata */}
        <Card style={styles.metadataCard}>
          <Typography variant="caption" style={styles.metadata}>
            Antigravity API Calls: {data.antigravity_calls || 0} •
            Execution Time: {data.execution_time_ms ? `${data.execution_time_ms.toFixed(0)}ms` : 'N/A'}
          </Typography>
        </Card>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 100,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
  },
  summaryCard: {
    marginBottom: 16,
    padding: 20,
  },
  cardTitle: {
    marginBottom: 12,
  },
  summaryText: {
    marginBottom: 20,
    lineHeight: 22,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  stat: {
    alignItems: 'center',
  },
  statLabel: {
    marginBottom: 4,
    opacity: 0.7,
  },
  statValue: {
    color: '#7c3aed',
  },
  sectionCard: {
    marginBottom: 12,
    padding: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  expandIcon: {
    fontSize: 16,
    opacity: 0.7,
  },
  sectionContent: {
    marginTop: 16,
  },
  infoRow: {
    marginBottom: 12,
  },
  label: {
    marginBottom: 4,
    opacity: 0.7,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 12,
  },
  tag: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
    marginRight: 8,
    marginBottom: 8,
  },
  insightCard: {
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    marginBottom: 12,
    backgroundColor: 'rgba(124, 58, 237, 0.05)',
  },
  insightHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  insightType: {
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 1,
    opacity: 0.7,
  },
  confidence: {
    opacity: 0.7,
  },
  insightTitle: {
    marginBottom: 8,
  },
  insightDesc: {
    lineHeight: 20,
    opacity: 0.9,
  },
  severityBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  reasoningStep: {
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderLeftWidth: 4,
    marginBottom: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
  },
  stepNumber: {
    marginBottom: 8,
    opacity: 0.7,
  },
  stepThought: {
    marginBottom: 6,
    lineHeight: 20,
  },
  stepAction: {
    marginBottom: 6,
    lineHeight: 20,
  },
  stepObservation: {
    lineHeight: 20,
    opacity: 0.8,
  },
  actionCard: {
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    marginBottom: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
  },
  actionTitle: {
    marginBottom: 8,
  },
  actionDesc: {
    marginBottom: 12,
    lineHeight: 20,
    opacity: 0.9,
  },
  actionFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  simCard: {
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    marginBottom: 12,
    backgroundColor: 'rgba(34, 197, 94, 0.05)',
  },
  simTitle: {
    marginBottom: 16,
  },
  simStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  simStat: {
    alignItems: 'center',
  },
  scenarios: {
    marginTop: 12,
  },
  scenarioLabel: {
    marginBottom: 4,
    opacity: 0.7,
  },
  impactGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  impactItem: {
    alignItems: 'center',
  },
  metadataCard: {
    padding: 12,
    marginBottom: 16,
  },
  metadata: {
    textAlign: 'center',
    opacity: 0.6,
  },
});
