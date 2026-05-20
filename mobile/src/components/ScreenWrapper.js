import React from 'react';
import { StyleSheet, View, SafeAreaView, StatusBar } from 'react-native';
import { useTheme } from '../hooks/useTheme';

export function ScreenWrapper({ children }) {
  const theme = useTheme();

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: theme.colors.backgroundPrimary }]}>
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.backgroundPrimary} />
      <View style={[styles.container, { backgroundColor: theme.colors.backgroundPrimary }]}>
        {children}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  container: {
    flex: 1,
  }
});
