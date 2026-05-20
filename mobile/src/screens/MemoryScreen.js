import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TextInput } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function MemoryScreen() {
  const theme = useTheme();
  const [searchQuery, setSearchQuery] = useState('');

  const memoryNodes = [
    { key: 'LAST_USER_INTENT', value: '"Optimize server load balancing across regions"', type: 'intent' },
    { key: 'ACTIVE_AGENTS', value: '[Planner, Architect, DevAgent, DebateAgent]', type: 'system' },
    { key: 'CONTEXT_WINDOW', value: '128K tokens | 94% utilized', type: 'system' },
    { key: 'RECENT_DECISION', value: 'Prioritize latency over throughput', type: 'decision' },
  ];

  return (
    <ScreenWrapper>
      <TopBar
        title="MEMORY VAULT"
        subtitle="🧠 Cognitive Storage"
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
            <Typography style={{ fontSize: 40 }}>🧠</Typography>
          </View>

          <Typography variant="h1" uppercase style={styles.headerTitle}>
            Context Buffer
          </Typography>

          <Typography variant="body" style={styles.headerSubtitle}>
            Current session active working memory state
          </Typography>
        </View>

        {/* Search Bar */}
        <View style={[styles.searchBar, {
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          borderColor: theme.colors.border,
        }]}>
          <Typography style={{ fontSize: 16 }}>🔍</Typography>
          <TextInput
            style={[styles.searchInput, { color: theme.colors.textBody }]}
            placeholder="Search memory nodes..."
            placeholderTextColor={theme.colors.textMuted}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {/* Memory Nodes */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Active Memory Nodes
        </Typography>

        {memoryNodes.map((node, index) => (
          <Card key={index} variant="default" style={styles.nodeCard}>
            <View style={styles.nodeHeader}>
              <Typography variant="tiny" uppercase style={[styles.nodeKey, {
                color: theme.colors.primaryNeon
              }]}>
                {node.key}
              </Typography>
              <View style={[styles.typeBadge, {
                backgroundColor: node.type === 'intent' ? 'rgba(252, 211, 77, 0.2)' :
                                 node.type === 'decision' ? 'rgba(124, 58, 237, 0.2)' :
                                 'rgba(16, 185, 129, 0.2)',
                borderColor: node.type === 'intent' ? 'rgba(252, 211, 77, 0.3)' :
                             node.type === 'decision' ? 'rgba(124, 58, 237, 0.3)' :
                             'rgba(16, 185, 129, 0.3)',
              }]}>
                <Typography variant="tiny" uppercase style={{
                  color: node.type === 'intent' ? theme.colors.accentGold :
                         node.type === 'decision' ? theme.colors.primaryNeon :
                         theme.colors.success
                }}>
                  {node.type}
                </Typography>
              </View>
            </View>
            <Typography variant="body" style={styles.nodeValue}>
              {node.value}
            </Typography>
          </Card>
        ))}

        {/* Actions */}
        <View style={styles.actions}>
          <Button variant="primary" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              EXPORT MEMORY
            </Typography>
          </Button>
          <Button variant="outline" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              CLEAR CACHE
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
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 24,
    gap: 10,
  },
  searchInput: {
    flex: 1,
    fontSize: 14,
    fontWeight: '600',
  },
  sectionTitle: {
    marginBottom: 16,
  },
  nodeCard: {
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#7C3AED',
  },
  nodeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  nodeKey: {
    flex: 1,
  },
  typeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    borderWidth: 1,
  },
  nodeValue: {
    fontFamily: 'monospace',
    lineHeight: 20,
  },
  actions: {
    gap: 12,
    marginTop: 24,
  },
  actionBtn: {
    width: '100%',
  },
});
