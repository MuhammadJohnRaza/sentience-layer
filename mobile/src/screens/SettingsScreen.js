import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, Switch } from 'react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { useTheme } from '../hooks/useTheme';
import { Typography } from '../components/Typography';

export function SettingsScreen() {
  const theme = useTheme();
  const [offlineSync, setOfflineSync] = useState(true);
  const [stealthMode, setStealthMode] = useState(false);
  const [computeBoost, setComputeBoost] = useState(true);
  const [notifications, setNotifications] = useState(true);

  return (
    <ScreenWrapper>
      <TopBar
        title="KERNEL SETTINGS"
        subtitle="⚙️ System Configuration"
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
            <Typography style={{ fontSize: 40 }}>⚙️</Typography>
          </View>

          <Typography variant="h1" uppercase style={styles.headerTitle}>
            System Configuration
          </Typography>
        </View>

        {/* Network & Sync */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Network & Sync
        </Typography>

        <Card variant="default" style={styles.settingCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <View style={[styles.settingIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 20 }}>📡</Typography>
              </View>
              <View style={styles.settingText}>
                <Typography variant="bodyBold">Offline-First Sync</Typography>
                <Typography variant="caption" style={styles.settingDesc}>
                  Queue actions while disconnected
                </Typography>
              </View>
            </View>
            <Switch
              value={offlineSync}
              onValueChange={setOfflineSync}
              trackColor={{ true: theme.colors.primaryNeon, false: 'rgba(255,255,255,0.1)' }}
              thumbColor={offlineSync ? theme.colors.accentGold : '#f4f3f4'}
            />
          </View>
        </Card>

        <Card variant="default" style={styles.settingCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <View style={[styles.settingIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 20 }}>🔔</Typography>
              </View>
              <View style={styles.settingText}>
                <Typography variant="bodyBold">Push Notifications</Typography>
                <Typography variant="caption" style={styles.settingDesc}>
                  Receive agent alerts and updates
                </Typography>
              </View>
            </View>
            <Switch
              value={notifications}
              onValueChange={setNotifications}
              trackColor={{ true: theme.colors.primaryNeon, false: 'rgba(255,255,255,0.1)' }}
              thumbColor={notifications ? theme.colors.accentGold : '#f4f3f4'}
            />
          </View>
        </Card>

        {/* Agent Preferences */}
        <Typography variant="h2" uppercase style={styles.sectionTitle}>
          Agent Preferences
        </Typography>

        <Card variant="default" style={styles.settingCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <View style={[styles.settingIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 20 }}>👁️</Typography>
              </View>
              <View style={styles.settingText}>
                <Typography variant="bodyBold">Stealth Mode</Typography>
                <Typography variant="caption" style={styles.settingDesc}>
                  Limit telemetry and logging
                </Typography>
              </View>
            </View>
            <Switch
              value={stealthMode}
              onValueChange={setStealthMode}
              trackColor={{ true: theme.colors.primaryNeon, false: 'rgba(255,255,255,0.1)' }}
              thumbColor={stealthMode ? theme.colors.accentGold : '#f4f3f4'}
            />
          </View>
        </Card>

        <Card variant="default" style={styles.settingCard}>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <View style={[styles.settingIcon, {
                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                borderColor: theme.colors.border,
              }]}>
                <Typography style={{ fontSize: 20 }}>⚡</Typography>
              </View>
              <View style={styles.settingText}>
                <Typography variant="bodyBold">Compute Boost</Typography>
                <Typography variant="caption" style={styles.settingDesc}>
                  Allocate max RAM to swarm operations
                </Typography>
              </View>
            </View>
            <Switch
              value={computeBoost}
              onValueChange={setComputeBoost}
              trackColor={{ true: theme.colors.primaryNeon, false: 'rgba(255,255,255,0.1)' }}
              thumbColor={computeBoost ? theme.colors.accentGold : '#f4f3f4'}
            />
          </View>
        </Card>

        {/* Actions */}
        <View style={styles.actions}>
          <Button variant="destructive" size="default" style={styles.actionBtn}>
            <Typography variant="button" uppercase>
              RESET TO DEFAULTS
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
  sectionTitle: {
    marginBottom: 16,
    marginTop: 8,
  },
  settingCard: {
    padding: 16,
    marginBottom: 12,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: 12,
    marginRight: 16,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  settingText: {
    flex: 1,
    gap: 4,
  },
  settingDesc: {
    opacity: 0.7,
  },
  actions: {
    gap: 12,
    marginTop: 32,
  },
  actionBtn: {
    width: '100%',
  },
});
