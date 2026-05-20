import React from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { Card } from './Card';
import { Typography } from './Typography';
import { useTheme } from '../hooks/useTheme';

export const ActionCard = ({ title, description, status = 'pending', onPress }) => {
  const theme = useTheme();

  const getStatusStyle = () => {
    switch (status) {
      case 'active':
        return {
          backgroundColor: 'rgba(16, 185, 129, 0.2)',
          borderColor: 'rgba(16, 185, 129, 0.3)',
          textColor: '#10B981',
        };
      case 'completed':
        return {
          backgroundColor: 'rgba(124, 58, 237, 0.2)',
          borderColor: 'rgba(124, 58, 237, 0.3)',
          textColor: theme.colors.primaryNeon,
        };
      case 'pending':
        return {
          backgroundColor: 'rgba(252, 211, 77, 0.2)',
          borderColor: 'rgba(252, 211, 77, 0.3)',
          textColor: theme.colors.accentGold,
        };
      default:
        return {
          backgroundColor: 'rgba(212, 212, 216, 0.2)',
          borderColor: 'rgba(212, 212, 216, 0.3)',
          textColor: theme.colors.textMuted,
        };
    }
  };

  const statusStyle = getStatusStyle();

  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      <Card style={styles.container}>
        <View style={styles.header}>
          <Typography variant="h3" uppercase style={styles.title}>
            {title}
          </Typography>
          <View style={[styles.statusBadge, {
            backgroundColor: statusStyle.backgroundColor,
            borderColor: statusStyle.borderColor,
          }]}>
            <Typography variant="tiny" uppercase style={[styles.statusText, {
              color: statusStyle.textColor
            }]}>
              {status}
            </Typography>
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
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  title: {
    flex: 1,
    marginRight: 12,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
  },
  statusText: {
  },
  description: {
    marginTop: 4,
    opacity: 0.9,
  },
});
