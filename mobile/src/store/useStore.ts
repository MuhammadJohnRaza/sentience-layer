import { create } from 'zustand';

interface StoreState {
  isOnline: boolean;
  offlineActions: any[];
  addOfflineAction: (action: any) => void;
  syncOfflineActions: () => Promise<void>;
  setOnlineStatus: (status: boolean) => void;
}

export const useStore = create<StoreState>((set, get) => ({
  isOnline: true,
  offlineActions: [],
  addOfflineAction: (action) => set((state) => ({ 
    offlineActions: [...state.offlineActions, action] 
  })),
  syncOfflineActions: async () => {
    const actions = get().offlineActions;
    if (actions.length === 0) return;
    
    // Simulate syncing to backend
    console.log(`Syncing ${actions.length} offline actions...`);
    set({ offlineActions: [] });
  },
  setOnlineStatus: (status) => set({ isOnline: status }),
}));
