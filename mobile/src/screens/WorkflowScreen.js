import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useWorkflow } from '../hooks/useWorkflow';
import { fetchWorkflows } from '../store/workflowSlice';

const STATUS_COLORS = {
  pending: '#f59e0b',
  processing: '#4f46e5',
  completed: '#10b981',
  failed: '#ef4444'
};

export default function WorkflowScreen() {
  const dispatch = useDispatch();
  const { workflows, loading } = useSelector(state => state.workflow);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const { refreshWorkflows } = useWorkflow();

  useEffect(() => {
    dispatch(fetchWorkflows());
  }, [dispatch]);

  const filteredWorkflows = selectedFilter === 'all' 
    ? workflows 
    : workflows.filter(w => w.status === selectedFilter);

  const renderFilters = () => (
    <ScrollView 
      horizontal 
      showsHorizontalScrollIndicator={false}
      style={styles.filterContainer}
      contentContainerStyle={styles.filterContent}
    >
      {['all', 'pending', 'processing', 'completed', 'failed'].map(filter => (
        <TouchableOpacity
          key={filter}
          style={[
            styles.filterButton,
            selectedFilter === filter && styles.filterButtonActive
          ]}
          onPress={() => setSelectedFilter(filter)}
        >
          <Text style={[
            styles.filterText,
            selectedFilter === filter && styles.filterTextActive
          ]}>
            {filter.charAt(0).toUpperCase() + filter.slice(1)}
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  const renderWorkflowCard = (workflow) => (
    <TouchableOpacity key={workflow.id} style={styles.workflowCard}>
      <View style={styles.workflowHeader}>
        <View style={styles.workflowTitleContainer}>
          <View style={[
            styles.statusIndicator,
            { backgroundColor: STATUS_COLORS[workflow.status] }
          ]} />
          <Text style={styles.workflowTitle} numberOfLines={1}>{workflow.title}</Text>
        </View>
        <Text style={[styles.statusBadge, { color: STATUS_COLORS[workflow.status] }]}>
          {workflow.status}
        </Text>
      </View>
      
      <Text style={styles.workflowDescription} numberOfLines={2}>
        {workflow.description}
      </Text>
      
      <View style={styles.workflowMeta}>
        <View style={styles.metaItem}>
          <Icon name="clock-outline" size={14} color="#6b6b8a" />
          <Text style={styles.metaText}>{workflow.duration || '0s'}</Text>
        </View>
        <View style={styles.metaItem}>
          <Icon name="robot" size={14} color="#6b6b8a" />
          <Text style={styles.metaText}>{workflow.agentCount || 0} agents</Text>
        </View>
        <View style={styles.metaItem}>
          <Icon name="lightning-bolt" size={14} color="#6b6b8a" />
          <Text style={styles.metaText}>{workflow.actions || 0} actions</Text>
        </View>
      </View>

      <View style={styles.progressContainer}>
        <View style={[styles.progressBar, { width: `${workflow.progress || 0}%` }]} />
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {renderFilters()}
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl
            refreshing={loading}
            onRefresh={refreshWorkflows}
            tintColor="#4f46e5"
          />
        }
      >
        {filteredWorkflows.length === 0 ? (
          <View style={styles.emptyState}>
            <Icon name="workflow" size={64} color="#2a2a4a" />
            <Text style={styles.emptyTitle}>No workflows yet</Text>
            <Text style={styles.emptySubtitle}>Create an input to start a workflow</Text>
          </View>
        ) : (
          filteredWorkflows.map(renderWorkflowCard)
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a1a'
  },
  filterContainer: {
    maxHeight: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#1a1a3e'
  },
  filterContent: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    gap: 8
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#1a1a3e',
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  filterButtonActive: {
    backgroundColor: '#4f46e520',
    borderColor: '#4f46e5'
  },
  filterText: {
    fontSize: 13,
    color: '#6b6b8a',
    fontWeight: '500'
  },
  filterTextActive: {
    color: '#4f46e5',
    fontWeight: '600'
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 16
  },
  workflowCard: {
    backgroundColor: '#1a1a3e',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  workflowHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8
  },
  workflowTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginRight: 12
  },
  statusIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8
  },
  workflowTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#e0e0ff',
    flex: 1
  },
  statusBadge: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase'
  },
  workflowDescription: {
    fontSize: 14,
    color: '#6b6b8a',
    lineHeight: 20,
    marginBottom: 12
  },
  workflowMeta: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 12
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4
  },
  metaText: {
    fontSize: 12,
    color: '#6b6b8a'
  },
  progressContainer: {
    height: 4,
    backgroundColor: '#0f0f23',
    borderRadius: 2,
    overflow: 'hidden'
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#4f46e5',
    borderRadius: 2
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 80
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#e0e0ff',
    marginTop: 16
  },
  emptySubtitle: {
    fontSize: 14,
    color: '#6b6b8a',
    marginTop: 8
  }
});