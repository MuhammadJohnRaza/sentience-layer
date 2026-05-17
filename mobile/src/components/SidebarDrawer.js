import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { Hexagon, LayoutDashboard, BrainCircuit, Activity, Settings, X } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';
const TEXT_MUTED = '#A7A7B5';

export function SidebarDrawer({ isOpen, onClose }) {
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
      <View style={styles.drawer}>
        <View style={styles.header}>
          <View style={styles.logoRow}>
            <Hexagon color={PRIMARY_NEON} size={24} style={styles.glow} />
            <Text style={styles.logoText}>SENTIENCE</Text>
          </View>
          <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
            <X color={TEXT_MUTED} size={20} />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.menu}>
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <TouchableOpacity key={index} style={styles.menuItem}>
                <Icon color={PRIMARY_NEON} size={20} />
                <Text style={styles.menuText}>{item.label}</Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
        
        <View style={styles.footer}>
          <Text style={styles.versionText}>Kernel v3.1.4</Text>
          <Text style={styles.statusText}>ALL SYSTEMS NOMINAL</Text>
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
    backgroundColor: '#0B0B12',
    borderRightWidth: 1,
    borderRightColor: 'rgba(122, 46, 255, 0.3)',
    shadowColor: PRIMARY_NEON,
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
    borderBottomColor: 'rgba(122, 46, 255, 0.15)',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  glow: {
    shadowColor: PRIMARY_NEON,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 10,
  },
  logoText: {
    color: TEXT_HIGHLIGHT,
    fontSize: 16,
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
    color: TEXT_HIGHLIGHT,
    fontSize: 14,
    fontWeight: '600',
    letterSpacing: 1,
  },
  footer: {
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: 'rgba(122, 46, 255, 0.15)',
    alignItems: 'center',
  },
  versionText: {
    color: TEXT_MUTED,
    fontSize: 12,
    fontFamily: 'monospace',
    marginBottom: 4,
  },
  statusText: {
    color: '#32D74B',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  }
});
