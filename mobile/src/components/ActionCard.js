import React from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { Card } from './Card';
import { Typography } from './Typography';
import { useTheme } from '../hooks/useTheme';

export const ActionCard = ({ title, description, status, onPress }) => {
  const theme = useTheme();

  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      <Card style={styles.container}>
        <View style={styles.header}>
          <Typography variant="h3">{title}</Typography>
          <View style={[styles.statusBadge, { backgroundColor: status === 'active' ? theme.colors.success : theme.colors.textMuted }]}>
            <Typography variant="muted" style={styles.statusText}>{status}</Typography>
          </View>
        </View>
        <Typography variant="body" style={styles.description}>
          {description}
        </Typography>
      </Card>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 10,
    color: '#000',
    fontWeight: 'bold',
  },
  description: {
    marginTop: 4,
  },
});
