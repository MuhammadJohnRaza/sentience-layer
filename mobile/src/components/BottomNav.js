import React from 'react';
import { StyleSheet, View, TouchableOpacity } from 'react-native';
import { Home, MessageSquare, BarChart3, Settings } from 'lucide-react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

export function BottomNav({ activeRoute = 'Home', onNavigate }) {
  const theme = useTheme();
  const tabs = [
    { name: 'Home', icon: Home, label: 'HOME' },
    { name: 'Chat', icon: MessageSquare, label: 'CHAT' },
    { name: 'Dashboard', icon: BarChart3, label: 'METRICS' },
    { name: 'Settings', icon: Settings, label: 'SETTINGS' },
  ];

  return (
    <View style={[styles.container, {
      backgroundColor: 'rgba(17, 17, 17, 0.95)',
      borderTopColor: theme.colors.border,
    }]}>
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeRoute === tab.name;

        return (
          <TouchableOpacity
            key={tab.name}
            style={styles.tab}
            onPress={() => onNavigate && onNavigate(tab.name)}
            activeOpacity={0.7}
          >
            <View style={[
              styles.iconWrapper,
              isActive && {
                backgroundColor: 'rgba(124, 58, 237, 0.2)',
                borderRadius: 12,
                padding: 8,
              }
            ]}>
              <Icon
                color={isActive ? theme.colors.primaryNeon : theme.colors.textMuted}
                size={24}
                style={[isActive && {
                  shadowColor: theme.colors.primaryNeon,
                  shadowOffset: { width: 0, height: 0 },
                  shadowOpacity: 0.8,
                  shadowRadius: 10,
                  elevation: 5,
                }]}
              />
            </View>
            <Typography
              variant="tiny"
              uppercase
              style={{
                color: isActive ? theme.colors.primaryNeon : theme.colors.textMuted,
                marginTop: 4,
              }}
            >
              {tab.label}
            </Typography>
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
    borderTopWidth: 1,
    paddingVertical: 8,
    paddingBottom: 24,
  },
  tab: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    paddingVertical: 4,
  },
  iconWrapper: {
    alignItems: 'center',
    justifyContent: 'center',
  },
});
