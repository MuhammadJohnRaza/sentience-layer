import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Activity } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';

export function MetricsCard({ title, value, trend, isPositive }) {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{title}</Text>
        <Activity color={PRIMARY_NEON} size={14} />
      </View>
      
      <View style={styles.content}>
        <Text style={styles.value}>{value}</Text>
        {trend && (
          <Text style={[styles.trend, isPositive ? styles.trendPos : styles.trendNeg]}>
            {isPositive ? '+' : '-'}{trend}
          </Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'rgba(11, 11, 18, 0.8)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.2)',
    flex: 1,
    marginHorizontal: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    color: '#A7A7B5',
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
  },
  value: {
    color: '#F5F5F7',
    fontSize: 24,
    fontWeight: '800',
  },
  trend: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 4,
  },
  trendPos: {
    color: '#32D74B',
  },
  trendNeg: {
    color: '#FF453A',
  }
});
