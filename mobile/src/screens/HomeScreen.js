import React from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

const { width } = Dimensions.get('window');

const MODULES = [
  { id: 'ContentInput', label: 'Content→Action', icon: '📄', desc: 'Upload & analyze', featured: true },
  { id: 'Dashboard', label: 'Dashboard', icon: '📊', desc: 'System overview' },
  { id: 'Chat', label: 'Cognitive Chat', icon: '💬', desc: 'Multi-agent reasoning' },
  { id: 'Causal', label: 'Causal Graph', icon: '🕸️', desc: 'Logic mapping' },
  { id: 'Simulation', label: 'Simulate', icon: '🎯', desc: 'Predictive modeling' },
  { id: 'Memory', label: 'Memory Vault', icon: '🧠', desc: 'Cognitive storage' },
  { id: 'Dreamscape', label: 'Dreamscape', icon: '🌌', desc: 'Offline synthesis' },
  { id: 'Economy', label: 'Economic', icon: '💰', desc: 'Value orchestration' },
  { id: 'Doubt', label: 'Doubt Room', icon: '🤔', desc: 'Confidence analysis' },
];

export default function HomeScreen({ navigation }) {
  const theme = useTheme();

  return (
    <ScreenWrapper>
      <TopBar
        title="SENTIENCE LAYER"
        subtitle="Cognitive Operating System"
        showStatus={false}
      />

      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        {/* Hero Section */}
        <View style={styles.hero}>
          <View style={[styles.heroIcon, {
            backgroundColor: 'rgba(124, 58, 237, 0.2)',
            borderColor: theme.colors.borderMedium,
            ...theme.shadows.neonGlow,
          }]}>
            <Typography style={{ fontSize: 48 }}>🔮</Typography>
          </View>

          <Typography variant="h1" uppercase style={styles.heroTitle}>
            Sentience Layer
          </Typography>

          <Typography variant="body" style={styles.heroSubtitle}>
            A Cognitive Operating System powered by Google Antigravity — where AI agents reason, simulate, and act with human-aligned intelligence.
          </Typography>
        </View>

        {/* Status Card */}
        <Card variant="elevated" style={styles.statusCard}>
          <View style={styles.statusContent}>
            <View style={[styles.statusIcon, {
              backgroundColor: 'rgba(16, 185, 129, 0.2)',
              borderColor: 'rgba(16, 185, 129, 0.3)',
            }]}>
              <Typography style={{ fontSize: 24 }}>✓</Typography>
            </View>
            <View style={styles.statusText}>
              <Typography variant="h3" uppercase>
                All Systems Nominal
              </Typography>
              <Typography variant="caption" style={styles.statusDetail}>
                18 Agents • 94% Self-Awareness
              </Typography>
            </View>
          </View>
        </Card>

        {/* Modules Section */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Cognitive Modules
        </Typography>

        <View style={styles.grid}>
          {MODULES.map(module => (
            <TouchableOpacity
              key={module.id}
              style={[styles.moduleCard, {
                backgroundColor: module.featured ? 'rgba(124, 58, 237, 0.2)' : theme.colors.card,
                borderColor: module.featured ? theme.colors.primary : theme.colors.border,
                borderWidth: module.featured ? 3 : 2,
              }]}
              onPress={() => navigation?.navigate(module.id)}
              activeOpacity={0.7}
            >
              <View style={[styles.iconContainer, {
                backgroundColor: module.featured ? 'rgba(124, 58, 237, 0.3)' : 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 28 }}>{module.icon}</Typography>
              </View>
              <Typography variant="h3" uppercase style={styles.moduleLabel}>
                {module.label}
              </Typography>
              <Typography variant="caption" style={styles.moduleDesc}>
                {module.desc}
              </Typography>
              {module.featured && (
                <View style={styles.featuredBadge}>
                  <Typography variant="caption" style={{ fontSize: 10 }}>
                    ⭐ COMPETITION DEMO
                  </Typography>
                </View>
              )}
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: {
    padding: 20,
    paddingBottom: 40,
  },
  hero: {
    alignItems: 'center',
    paddingVertical: 32,
    gap: 16,
  },
  heroIcon: {
    width: 96,
    height: 96,
    borderRadius: 48,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  heroTitle: {
    textAlign: 'center',
    fontSize: 32,
  },
  heroSubtitle: {
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 16,
    opacity: 0.9,
  },
  statusCard: {
    marginVertical: 24,
    padding: 20,
  },
  statusContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  statusIcon: {
    width: 48,
    height: 48,
    borderRadius: 16,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusText: {
    flex: 1,
    gap: 4,
  },
  statusDetail: {
    opacity: 0.7,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -6,
  },
  moduleCard: {
    width: (width - 52) / 2,
    borderRadius: 16,
    padding: 20,
    borderWidth: 2,
    marginHorizontal: 6,
    marginBottom: 12,
  },
  iconContainer: {
    width: 56,
    height: 56,
    borderRadius: 16,
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  moduleLabel: {
    fontSize: 14,
    marginBottom: 4,
  },
  moduleDesc: {
    opacity: 0.7,
  },
  featuredBadge: {
    marginTop: 8,
    paddingVertical: 4,
    paddingHorizontal: 8,
    backgroundColor: 'rgba(251, 191, 36, 0.2)',
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
});
