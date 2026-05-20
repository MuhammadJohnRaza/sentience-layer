/**
 * Git Sync Service
 * Handles version control and cloud synchronization
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

class GitSyncService {
  constructor() {
    this.syncQueue = [];
    this.isSyncing = false;
    this.lastSyncTime = null;
  }

  /**
   * Initialize git repository (mock for mobile)
   */
  async initRepository() {
    try {
      const repoInfo = await AsyncStorage.getItem('git_repo_info');
      if (!repoInfo) {
        const info = {
          initialized: true,
          branch: 'main',
          commits: [],
          remoteUrl: null,
          lastSync: null,
        };
        await AsyncStorage.setItem('git_repo_info', JSON.stringify(info));
      }
      return true;
    } catch (error) {
      console.error('Git init failed:', error);
      return false;
    }
  }

  /**
   * Commit changes locally
   */
  async commit(message, changes) {
    try {
      const repoInfo = await this.getRepoInfo();
      const commit = {
        id: Date.now().toString(),
        message,
        timestamp: new Date().toISOString(),
        changes,
        author: 'mobile_user',
      };

      repoInfo.commits.push(commit);
      await AsyncStorage.setItem('git_repo_info', JSON.stringify(repoInfo));

      // Add to sync queue
      this.syncQueue.push(commit);

      return commit;
    } catch (error) {
      console.error('Commit failed:', error);
      throw error;
    }
  }

  /**
   * Sync with remote (backend)
   */
  async sync() {
    if (this.isSyncing) {
      return { status: 'already_syncing' };
    }

    this.isSyncing = true;

    try {
      const repoInfo = await this.getRepoInfo();

      // Push local commits to backend
      if (this.syncQueue.length > 0) {
        // In production, this would call the backend API
        console.log(`Syncing ${this.syncQueue.length} commits to backend...`);

        // Mock sync delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Clear sync queue
        this.syncQueue = [];
        repoInfo.lastSync = new Date().toISOString();
        await AsyncStorage.setItem('git_repo_info', JSON.stringify(repoInfo));
      }

      this.lastSyncTime = new Date();
      return {
        status: 'success',
        syncedCommits: this.syncQueue.length,
        lastSync: this.lastSyncTime,
      };
    } catch (error) {
      console.error('Sync failed:', error);
      return {
        status: 'error',
        error: error.message,
      };
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Get repository info
   */
  async getRepoInfo() {
    try {
      const info = await AsyncStorage.getItem('git_repo_info');
      return info ? JSON.parse(info) : null;
    } catch (error) {
      console.error('Failed to get repo info:', error);
      return null;
    }
  }

  /**
   * Get commit history
   */
  async getCommitHistory(limit = 10) {
    try {
      const repoInfo = await this.getRepoInfo();
      if (!repoInfo) return [];

      return repoInfo.commits.slice(-limit).reverse();
    } catch (error) {
      console.error('Failed to get commit history:', error);
      return [];
    }
  }

  /**
   * Auto-sync on interval
   */
  startAutoSync(intervalMinutes = 5) {
    setInterval(() => {
      if (this.syncQueue.length > 0) {
        this.sync();
      }
    }, intervalMinutes * 60 * 1000);
  }

  /**
   * Save insight to version control
   */
  async saveInsight(insight) {
    try {
      const insights = await this.getInsights();
      insights.push({
        ...insight,
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
      });

      await AsyncStorage.setItem('insights', JSON.stringify(insights));

      // Commit the change
      await this.commit(`Add insight: ${insight.title}`, {
        type: 'insight',
        data: insight,
      });

      return true;
    } catch (error) {
      console.error('Failed to save insight:', error);
      return false;
    }
  }

  /**
   * Save action to version control
   */
  async saveAction(action) {
    try {
      const actions = await this.getActions();
      actions.push({
        ...action,
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
      });

      await AsyncStorage.setItem('actions', JSON.stringify(actions));

      // Commit the change
      await this.commit(`Add action: ${action.title}`, {
        type: 'action',
        data: action,
      });

      return true;
    } catch (error) {
      console.error('Failed to save action:', error);
      return false;
    }
  }

  /**
   * Save simulation result to version control
   */
  async saveSimulation(simulation) {
    try {
      const simulations = await this.getSimulations();
      simulations.push({
        ...simulation,
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
      });

      await AsyncStorage.setItem('simulations', JSON.stringify(simulations));

      // Commit the change
      await this.commit(`Add simulation: ${simulation.action_title}`, {
        type: 'simulation',
        data: simulation,
      });

      return true;
    } catch (error) {
      console.error('Failed to save simulation:', error);
      return false;
    }
  }

  /**
   * Get saved insights
   */
  async getInsights() {
    try {
      const data = await AsyncStorage.getItem('insights');
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Failed to get insights:', error);
      return [];
    }
  }

  /**
   * Get saved actions
   */
  async getActions() {
    try {
      const data = await AsyncStorage.getItem('actions');
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Failed to get actions:', error);
      return [];
    }
  }

  /**
   * Get saved simulations
   */
  async getSimulations() {
    try {
      const data = await AsyncStorage.getItem('simulations');
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Failed to get simulations:', error);
      return [];
    }
  }

  /**
   * Clear all local data
   */
  async clearAll() {
    try {
      await AsyncStorage.multiRemove([
        'git_repo_info',
        'insights',
        'actions',
        'simulations',
      ]);
      this.syncQueue = [];
      return true;
    } catch (error) {
      console.error('Failed to clear data:', error);
      return false;
    }
  }
}

export default new GitSyncService();
