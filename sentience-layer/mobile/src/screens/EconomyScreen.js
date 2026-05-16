import React from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { BarChart } from 'react-native-chart-kit';

const { width } = Dimensions.get('window');

const ASSETS = [
  { id: '1', name: 'Computational Credit', balance: '1,420', trend: '+4.2%' },
  { id: '2', name: 'Knowledge Tokens', balance: '850', trend: '+12.5%' },
  { id: '3', name: 'Priority Weights', balance: '240', trend: '-2.1%' }
];

export default function EconomyScreen() {
  const chartConfig = {
    backgroundGradientFrom: '#1a1a3e',
    backgroundGradientTo: '#1a1a3e',
    color: (opacity = 1) => `rgba(251, 146, 60, ${opacity})`,
    barPercentage: 0.6
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.title}>Economic Model</Text>
        <Text style={styles.subtitle}>Resource allocation and value orchestration</Text>
      </View>

      <View style={styles.summaryCard}>
        <Text style={styles.summaryLabel}>Total System Value</Text>
        <Text style={styles.summaryValue}>2,510 $SENT</Text>
        <View style={styles.trendBadge}>
          <Icon name="trending-up" size={14} color="#10b981" />
          <Text style={styles.trendText}>+8.4% last 24h</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Asset Allocation</Text>
      <View style={styles.chartContainer}>
        <BarChart
          data={{
            labels: ['Comp', 'Know', 'Prio', 'Band'],
            datasets: [{ data: [80, 45, 28, 60] }]
          }}
          width={width - 72}
          height={180}
          chartConfig={chartConfig}
          style={styles.chart}
          fromZero
        />
      </View>

      <Text style={styles.sectionTitle}>Vault Assets</Text>
      {ASSETS.map(asset => (
        <View key={asset.id} style={styles.assetCard}>
          <View style={styles.assetIcon}>
            <Icon name="database" size={20} color="#fb923c" />
          </View>
          <View style={styles.assetInfo}>
            <Text style={styles.assetName}>{asset.name}</Text>
            <Text style={styles.assetBalance}>{asset.balance}</Text>
          </View>
          <Text style={[styles.assetTrend, { color: asset.trend.startsWith('+') ? '#10b981' : '#ef4444' }]}>
            {asset.trend}
          </Text>
        </View>
      ))}

      <View style={styles.orchestrationBox}>
        <Icon name="tune" size={24} color="#e0e0ff" />
        <Text style={styles.orchTitle}>Orchestration Active</Text>
        <Text style={styles.orchDesc}>Redistributing compute resources to Causal Agent based on current entropy.</Text>
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
  summaryCard: {
    backgroundColor: '#fb923c15',
    marginHorizontal: 20,
    padding: 24,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#fb923c40',
    alignItems: 'center',
    marginBottom: 24
  },
  summaryLabel: {
    color: '#fb923c',
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1
  },
  summaryValue: {
    color: '#e0e0ff',
    fontSize: 36,
    fontWeight: '900',
    marginVertical: 8
  },
  trendBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6
  },
  trendText: {
    color: '#10b981',
    fontSize: 12,
    fontWeight: '600'
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginHorizontal: 20,
    marginBottom: 16
  },
  chartContainer: {
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
    borderColor: '#2a2a4a',
    marginBottom: 24
  },
  chart: {
    marginLeft: -10,
    borderRadius: 12
  },
  assetCard: {
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
  assetIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: '#fb923c10',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16
  },
  assetInfo: {
    flex: 1
  },
  assetName: {
    fontSize: 14,
    color: '#6b6b8a'
  },
  assetBalance: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#e0e0ff'
  },
  assetTrend: {
    fontSize: 12,
    fontWeight: 'bold'
  },
  orchestrationBox: {
    backgroundColor: '#1a1a3e',
    marginHorizontal: 20,
    marginTop: 20,
    padding: 24,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#fb923c30',
    alignItems: 'center'
  },
  orchTitle: {
    color: '#e0e0ff',
    fontSize: 16,
    fontWeight: 'bold',
    marginVertical: 8
  },
  orchDesc: {
    color: '#6b6b8a',
    fontSize: 12,
    textAlign: 'center',
    lineHeight: 18
  }
});
