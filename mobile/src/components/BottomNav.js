import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import { Home, Hexagon, Activity, Settings } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_MUTED = '#A7A7B5';

export function BottomNav({ activeRoute = 'Home', onNavigate }) {
  const tabs = [
    { name: 'Home', icon: Home },
    { name: 'Kernel', icon: Hexagon },
    { name: 'Metrics', icon: Activity },
    { name: 'Settings', icon: Settings },
  ];

  return (
    <View style={styles.container}>
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeRoute === tab.name;
        
        return (
          <TouchableOpacity 
            key={tab.name} 
            style={styles.tab}
            onPress={() => onNavigate && onNavigate(tab.name)}
          >
            <Icon 
              color={isActive ? PRIMARY_NEON : TEXT_MUTED} 
              size={24} 
              style={isActive && styles.activeIcon}
            />
            {isActive && <View style={styles.activeDot} />}
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: '#050505',
    borderTopWidth: 1,
    borderTopColor: 'rgba(122, 46, 255, 0.15)',
    paddingVertical: 12,
    paddingBottom: 24, // Safe area for iPhone
  },
  tab: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
  },
  activeIcon: {
    shadowColor: PRIMARY_NEON,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 10,
    elevation: 5,
  },
  activeDot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: PRIMARY_NEON,
    marginTop: 4,
    shadowColor: PRIMARY_NEON,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 1,
    shadowRadius: 5,
  }
});
