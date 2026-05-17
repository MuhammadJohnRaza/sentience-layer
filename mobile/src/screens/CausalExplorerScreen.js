import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { Network, ArrowRight } from 'lucide-react-native';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';

const PRIMARY_NEON = '#7A2EFF';
const TEXT_HIGHLIGHT = '#F5F5F7';

export function CausalExplorerScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="CAUSAL EXPLORER" />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.headerBox}>
          <Network color={PRIMARY_NEON} size={32} />
          <Text style={styles.title}>CAUSAL GRAPH VIEW</Text>
          <Text style={styles.subtitle}>Interactive visualization of cause-and-effect pathways identified by the agent kernel.</Text>
        </View>

        <View style={styles.graphContainer}>
          <View style={styles.node}>
            <Text style={styles.nodeText}>Market Shift</Text>
          </View>
          <ArrowRight color="rgba(122, 46, 255, 0.5)" size={24} style={styles.arrow} />
          <View style={styles.node}>
            <Text style={styles.nodeText}>Risk Detected</Text>
          </View>
          <ArrowRight color="rgba(122, 46, 255, 0.5)" size={24} style={styles.arrow} />
          <View style={[styles.node, styles.actionNode]}>
            <Text style={styles.actionNodeText}>Hedge Protocol</Text>
          </View>
        </View>

        <View style={styles.insightBox}>
          <Text style={styles.insightTitle}>KERNEL INSIGHT</Text>
          <Text style={styles.insightText}>
            The system has identified a 82% correlation between the current market shift and historical latency events. Activating the Hedge Protocol is causally linked to a 45% reduction in potential exposure.
          </Text>
        </View>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  scroll: { padding: 16 },
  headerBox: { alignItems: 'center', marginBottom: 40, marginTop: 20 },
  title: { color: TEXT_HIGHLIGHT, fontSize: 20, fontWeight: '800', letterSpacing: 2, marginTop: 16, textShadowColor: 'rgba(122, 46, 255, 0.5)', textShadowOffset: { width: 0, height: 0 }, textShadowRadius: 10 },
  subtitle: { color: '#A7A7B5', fontSize: 12, textAlign: 'center', marginTop: 8, lineHeight: 18 },
  graphContainer: { alignItems: 'center', paddingVertical: 20, marginBottom: 40, backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: 20, borderWidth: 1, borderColor: 'rgba(255,255,255,0.05)' },
  node: { backgroundColor: 'rgba(255,255,255,0.05)', paddingHorizontal: 16, paddingVertical: 12, borderRadius: 12, borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)' },
  nodeText: { color: '#A7A7B5', fontSize: 12, fontWeight: '600', letterSpacing: 1 },
  arrow: { marginVertical: 16, transform: [{ rotate: '90deg' }] },
  actionNode: { backgroundColor: 'rgba(122,46,255,0.15)', borderColor: PRIMARY_NEON, shadowColor: PRIMARY_NEON, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.5, shadowRadius: 10, elevation: 5 },
  actionNodeText: { color: TEXT_HIGHLIGHT, fontSize: 14, fontWeight: '700', letterSpacing: 1 },
  insightBox: { backgroundColor: 'rgba(122,46,255,0.05)', padding: 16, borderRadius: 16, borderWidth: 1, borderLeftWidth: 4, borderColor: PRIMARY_NEON },
  insightTitle: { color: PRIMARY_NEON, fontSize: 10, fontWeight: '800', letterSpacing: 1.5, marginBottom: 8 },
  insightText: { color: '#A7A7B5', fontSize: 13, lineHeight: 20 }
});
