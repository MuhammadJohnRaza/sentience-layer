import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Hexagon, WifiOff, Bell } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';

export function TopBar({ title = 'SENTIENCE', isOffline = true }) {
  return (
    <View style={styles.container}>
      <View style={styles.leftSection}>
        <Hexagon color={PRIMARY_NEON} size={20} style={styles.glowIcon} />
        <Text style={styles.title}>{title}</Text>
      </View>
      
      <View style={styles.rightSection}>
        {isOffline && (
          <View style={styles.statusBadge}>
            <WifiOff color="#F6C344" size={12} />
            <Text style={styles.statusText}>OFFLINE</Text>
          </View>
        )}
        <TouchableOpacity style={styles.iconBtn}>
          <Bell color="#A7A7B5" size={20} />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: '#050505',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(122, 46, 255, 0.15)',
  },
  leftSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  glowIcon: {
    shadowColor: PRIMARY_NEON,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 10,
  },
  title: {
    color: '#F5F5F7',
    fontSize: 16,
    fontWeight: '800',
    letterSpacing: 1.5,
  },
  rightSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(246, 195, 68, 0.1)',
    paddingHorizontal: 6,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(246, 195, 68, 0.3)',
    gap: 4,
  },
  statusText: {
    color: '#F6C344',
    fontSize: 9,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  iconBtn: {
    padding: 4,
  }
});
