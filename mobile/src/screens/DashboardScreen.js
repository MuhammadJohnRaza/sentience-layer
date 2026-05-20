import React, { useEffect, useState } from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity } from 'react-native';
import { Activity, TrendingUp, Users, Zap } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { MetricsCard } from '../components/MetricsCard';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function DashboardScreen() {
  const theme = useTheme();
  const [metrics, setMetrics] = useState([
    {
      label: 'Active Agents',
      value: 12,
      change: 12,
      trend: 'up',
    },
    {
      label: 'Insights Today',
      value: 24,
      change: 8,
      trend: 'up',
    },
    {
      label: 'Actions Executed',
      value: 156,
      change: -3,
      trend: 'down',
    },
    {
      label: 'System Health',
      value: '98.5%',
      change: 0.2,
      trend: 'up',
    },
  ]);

  const recentActivity = [
    { id: 1, icon: '⚡', text: 'Swarm successfully handled API spike', time: '2m ago' },
    { id: 2, icon: '📊', text: 'Economic yield target adjusted', time: '15m ago' },
    { id: 3, icon: '🔍', text: 'Causal analysis completed', time: '1h ago' },
  ];

  return (
    <ScreenWrapper>
      <TopBar
        title="EXECUTIVE DASHBOARD"
        subtitle="Real-time system overview"
        showStatus={true}
      />

      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Page Header */}
        <View style={styles.header}>
          <Typography variant="h1" uppercase>
            Dashboard
          </Typography>
          <Typography variant="body" style={styles.subtitle}>
            Real-time system overview and key metrics
          </Typography>
        </View>

        {/* Metrics Grid */}
        <View style={styles.metricsGrid}>
          {metrics.map((metric, index) => (
            <View key={index} style={styles.metricWrapper}>
              <MetricsCard
                title={metric.label}
                value={metric.value}
                change={metric.change}
                trend={metric.trend}
              />
            </View>
          ))}
        </View>

        {/* Recent Activity Section */}
        <View style={styles.section}>
          <Typography variant="h2" uppercase style={styles.sectionTitle}>
            Recent Activity
          </Typography>

          <Card variant="elevated" style={styles.activityCard}>
            {recentActivity.map((activity, index) => (
              <View
                key={activity.id}
                style={[
                  styles.activityRow,
                  index < recentActivity.length - 1 && {
                    borderBottomWidth: 1,
                    borderBottomColor: 'rgba(124, 58, 237, 0.1)',
                  }
                ]}
              >
                <View style={[styles.activityIcon, {
                  backgroundColor: 'rgba(124, 58, 237, 0.2)',
                  borderColor: theme.colors.border,
                }]}>
                  <Typography style={{ fontSize: 16 }}>{activity.icon}</Typography>
                </View>
                <View style={styles.activityContent}>
                  <Typography variant="bodyBold" style={styles.activityText}>
                    {activity.text}
                  </Typography>
                  <Typography variant="caption" style={styles.activityTime}>
                    {activity.time}
                  </Typography>
                </View>
              </View>
            ))}
          </Card>
        </View>

        {/* CTA Button */}
        <Button
          variant="primary"
          size="lg"
          style={styles.ctaButton}
        >
          <Typography variant="button" uppercase>
            VIEW FULL TELEMETRY
          </Typography>
          <Typography style={{ fontSize: 16 }}>→</Typography>
        </Button>
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
    marginBottom: 24,
  },
  subtitle: {
    marginTop: 4,
    opacity: 0.8,
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -4,
    marginBottom: 24,
  },
  metricWrapper: {
    width: '50%',
    paddingHorizontal: 4,
    marginBottom: 8,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  activityCard: {
    padding: 0,
  },
  activityRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 12,
  },
  activityIcon: {
    width: 40,
    height: 40,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  activityContent: {
    flex: 1,
    gap: 4,
  },
  activityText: {
    lineHeight: 20,
  },
  activityTime: {
    opacity: 0.6,
  },
  ctaButton: {
    marginTop: 8,
  },
});
