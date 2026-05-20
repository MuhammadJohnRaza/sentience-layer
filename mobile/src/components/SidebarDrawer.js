import React from 'react';
import { StyleSheet, View, TouchableOpacity, ScrollView } from 'react-native';
import { Hexagon, LayoutDashboard, BrainCircuit, Activity, Settings, X } from 'lucide-react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

export function SidebarDrawer({ isOpen, onClose }) {
  const theme = useTheme();
  if (!isOpen) return null;

  const menuItems = [
    { label: 'Mission Control', icon: LayoutDashboard },
    { label: 'Cognitive Engine', icon: BrainCircuit },
    { label: 'System Health', icon: Activity },
    { label: 'Kernel Settings', icon: Settings },
  ];

  return (
    <View style={styles.overlay}>
      <TouchableOpacity style={styles.backdrop} onPress={onClose} />
      <View style={[styles.drawer, { backgroundColor: theme.colors.backgroundSecondary, borderRightColor: theme.colors.border, shadowColor: theme.colors.primaryNeon }]}>
        <View style={[styles.header, { borderBottomColor: theme.colors.border }]}>
          <View style={styles.logoRow}>
            <Hexagon
              color={theme.colors.primaryNeon}
              size={24}
              style={{
                shadowColor: theme.colors.primaryNeon,
                shadowOffset: { width: 0, height: 0 },
                shadowOpacity: 0.8,
                shadowRadius: 10,
              }}
            />
            <Typography variant="h2" style={styles.logoText}>SENTIENCE</Typography>
          </View>
          <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
            <X color={theme.colors.textMuted} size={20} />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.menu}>
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <TouchableOpacity key={index} style={styles.menuItem}>
                <Icon color={theme.colors.primaryNeon} size={20} />
                <Typography variant="body" style={styles.menuText}>{item.label}</Typography>
              </TouchableOpacity>
            );
          })}
        </ScrollView>

        <View style={[styles.footer, { borderTopColor: theme.colors.border }]}>
          <Typography variant="caption" style={styles.versionText}>Kernel v3.1.4</Typography>
          <Typography variant="caption" style={[styles.statusText, { color: theme.colors.success }]}>ALL SYSTEMS NOMINAL</Typography>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0, left: 0, right: 0, bottom: 0,
    flexDirection: 'row',
    zIndex: 100,
  },
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  drawer: {
    width: '75%',
    borderRightWidth: 1,
    shadowOffset: { width: 5, height: 0 },
    shadowOpacity: 0.2,
    shadowRadius: 20,
    elevation: 20,
    paddingTop: 50,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 20,
    borderBottomWidth: 1,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  logoText: {
    fontWeight: '800',
    letterSpacing: 2,
  },
  closeBtn: {
    padding: 4,
  },
  menu: {
    padding: 20,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.05)',
  },
  menuText: {
    fontWeight: '600',
    letterSpacing: 1,
  },
  footer: {
    padding: 20,
    borderTopWidth: 1,
    alignItems: 'center',
  },
  versionText: {
    fontFamily: 'monospace',
    marginBottom: 4,
  },
  statusText: {
    fontWeight: '700',
    letterSpacing: 1,
  }
});
