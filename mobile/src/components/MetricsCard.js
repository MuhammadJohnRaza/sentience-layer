import React from 'react';
import { StyleSheet, View } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';
import { Card } from './Card';

export function MetricsCard({ title, value, change, trend = 'neutral', icon }) {
  const theme = useTheme();

  const getTrendStyle = () => {
    switch (trend) {
      case 'up':
        return {
          backgroundColor: 'rgba(16, 185, 129, 0.2)',
          borderColor: 'rgba(16, 185, 129, 0.2)',
          textColor: '#10B981',
          icon: '▲',
        };
      case 'down':
        return {
          backgroundColor: 'rgba(244, 63, 94, 0.2)',
          borderColor: 'rgba(244, 63, 94, 0.2)',
          textColor: '#F43F5E',
          icon: '▼',
        };
      default:
        return {
          backgroundColor: 'rgba(124, 58, 237, 0.1)',
          borderColor: 'rgba(124, 58, 237, 0.2)',
          textColor: theme.colors.textMuted,
          icon: '',
        };
    }
  };

  const trendStyle = getTrendStyle();

  return (
    <Card style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <Typography variant="tiny" uppercase style={styles.title}>
            {title}
          </Typography>
        </View>

        <Typography variant="h1" style={styles.value}>
          {value}
        </Typography>

        {change !== undefined && (
          <View style={[styles.trendBadge, {
            backgroundColor: trendStyle.backgroundColor,
            borderColor: trendStyle.borderColor,
          }]}>
            <Typography variant="tiny" style={{ color: trendStyle.textColor }}>
              {trendStyle.icon} {Math.abs(change)}%
            </Typography>
          </View>
        )}
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginHorizontal: 4,
    padding: 20,
  },
  content: {
    gap: 8,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    color: '#D4D4D8',
  },
  value: {
    fontSize: 32,
    marginVertical: 4,
  },
  trendBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
  },
});
