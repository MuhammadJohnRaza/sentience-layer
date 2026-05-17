import React, { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, Switch } from 'react-native';
import { Settings, Cpu, Wifi, Eye } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function SettingsScreen() {
  const [offlineSync, setOfflineSync] = useState(true);
  const [stealthMode, setStealthMode] = useState(false);
  const [computeBoost, setComputeBoost] = useState(true);

  return (
    <ScreenWrapper>
      <TopBar title="KERNEL SETTINGS" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <Settings color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>SYSTEM CONFIGURATION</Text>
        </View>

        <View style={styles.settingGroup}>
          <Text style={styles.groupTitle}>NETWORK & SYNC</Text>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <Wifi color={PRIMARY_NEON} size={20} />
              <View>
                <Text style={styles.settingLabel}>Offline-First Sync</Text>
                <Text style={styles.settingDesc}>Queue actions while disconnected</Text>
              </View>
            </View>
            <Switch value={offlineSync} onValueChange={setOfflineSync} trackColor={{ true: PRIMARY_NEON, false: 'rgba(255,255,255,0.1)' }} />
          </View>
        </View>

        <View style={styles.settingGroup}>
          <Text style={styles.groupTitle}>AGENT PREFERENCES</Text>
          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <Eye color={PRIMARY_NEON} size={20} />
              <View>
                <Text style={styles.settingLabel}>Stealth Mode</Text>
                <Text style={styles.settingDesc}>Limit telemetry and logging</Text>
              </View>
            </View>
            <Switch value={stealthMode} onValueChange={setStealthMode} trackColor={{ true: PRIMARY_NEON, false: 'rgba(255,255,255,0.1)' }} />
          </View>

          <View style={styles.settingRow}>
            <View style={styles.settingLeft}>
              <Cpu color={PRIMARY_NEON} size={20} />
              <View>
                <Text style={styles.settingLabel}>Compute Boost</Text>
                <Text style={styles.settingDesc}>Allocate max RAM to swarm operations</Text>
              </View>
            </View>
            <Switch value={computeBoost} onValueChange={setComputeBoost} trackColor={{ true: PRIMARY_NEON, false: 'rgba(255,255,255,0.1)' }} />
          </View>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 40, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 18, fontWeight: '800', letterSpacing: 2, marginTop: 16 },
  settingGroup: { marginBottom: 30 },
  groupTitle: { color: PRIMARY_NEON, fontSize: 11, fontWeight: '800', letterSpacing: 1.5, marginBottom: 12, marginLeft: 4 },
  settingRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.03)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(122,46,255,0.15)', marginBottom: 8 },
  settingLeft: { flexDirection: 'row', alignItems: 'center', gap: 12, flex: 1 },
  settingLabel: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '600' },
  settingDesc: { color: '#A7A7B5', fontSize: 11, marginTop: 2 }
});
