import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Database, Lock, Fingerprint } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#00E5FF'; // Cyan for Vault
const TEXT_HIGHLIGHT = '#F5F5F7';

export function VaultScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="THE VAULT" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <Database color={PRIMARY_NEON} size={40} style={styles.glow} />
          <Text style={styles.title}>LONG-TERM MEMORY</Text>
          <Text style={styles.subtitle}>Encrypted latent space storage and immutable truths.</Text>
        </View>

        <TouchableOpacity style={styles.vaultItem}>
          <View style={styles.itemIcon}>
            <Lock color={PRIMARY_NEON} size={20} />
          </View>
          <View style={styles.itemContent}>
            <Text style={styles.itemTitle}>Core Directives</Text>
            <Text style={styles.itemSize}>4.2 MB • Encrypted</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.vaultItem}>
          <View style={styles.itemIcon}>
            <Fingerprint color={PRIMARY_NEON} size={20} />
          </View>
          <View style={styles.itemContent}>
            <Text style={styles.itemTitle}>Identity Matrix</Text>
            <Text style={styles.itemSize}>1.8 GB • Verified</Text>
          </View>
        </TouchableOpacity>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 40, marginTop: 20 },
  glow: { shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 20, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(0, 229, 255, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8 },
  vaultItem: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(0, 229, 255, 0.05)', padding: 16, borderRadius: 16, borderWidth: 1, borderColor: 'rgba(0, 229, 255, 0.2)', marginBottom: 12 },
  itemIcon: { width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(0, 229, 255, 0.1)', alignItems: 'center', justifyContent: 'center', marginRight: 16 },
  itemContent: { flex: 1 },
  itemTitle: { color: TEXT_HIGHLIGHT, fontSize: 16, fontWeight: '700', marginBottom: 4 },
  itemSize: { color: '#A7A7B5', fontSize: 11, fontWeight: '600', letterSpacing: 0.5 }
});
