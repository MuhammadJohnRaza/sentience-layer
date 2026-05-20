import React from 'react';
import { StyleSheet, View, TouchableOpacity } from 'react-native';
import { useTheme } from '../hooks/useTheme';
import { Typography } from './Typography';

export function TopBar({ title = 'SENTIENCE', subtitle, showStatus = true, onMenuPress }) {
  const theme = useTheme();

  return (
    <View style={[styles.container, {
      backgroundColor: 'rgba(17, 17, 17, 0.6)',
      borderBottomColor: theme.colors.border,
    }]}>
      <View style={styles.leftSection}>
        <View style={[styles.iconContainer, {
          backgroundColor: 'rgba(124, 58, 237, 0.2)',
          borderColor: theme.colors.border,
          shadowColor: theme.colors.primaryNeon,
          shadowOffset: { width: 0, height: 0 },
          shadowOpacity: 0.3,
          shadowRadius: 12,
          elevation: 5,
        }]}>
          <Typography style={{ fontSize: 20 }}>💬</Typography>
        </View>
        <View>
          <Typography variant="h3" uppercase style={styles.title}>
            {title}
          </Typography>
          {subtitle && (
            <View style={styles.subtitleRow}>
              <View style={styles.statusDot} />
              <Typography variant="tiny" uppercase style={styles.subtitle}>
                {subtitle}
              </Typography>
            </View>
          )}
        </View>
      </View>

      <View style={styles.rightSection}>
        {showStatus && (
          <View style={[styles.statusBadge, {
            backgroundColor: 'rgba(16, 185, 129, 0.2)',
            borderColor: 'rgba(16, 185, 129, 0.3)',
          }]}>
            <View style={[styles.statusDot, { backgroundColor: '#10B981' }]} />
            <Typography variant="tiny" uppercase style={{ color: '#10B981' }}>
              ACTIVE
            </Typography>
          </View>
        )}
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
    borderBottomWidth: 1,
  },
  leftSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 12,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontWeight: '800',
  },
  subtitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 2,
  },
  subtitle: {
    color: '#D4D4D8',
  },
  rightSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
    gap: 6,
  },
  statusDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#10B981',
  },
});
