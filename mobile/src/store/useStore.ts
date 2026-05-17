/** * Zustand Global Store
for Sentience Layer * Handles global state: user, theme, sidebar, notifications */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import {
  User,
  UserPreferences,
  Message,
  Insight,
  Action,
  AgentTrace,
} from "@/types";
interface AppState {
  // User
  user: User | null;
  setUser: (user: User | null) => void;
  // Theme
  theme: "light" | "dark" | "system";
  setTheme: (theme: "light" | "dark" | "system") => void;
  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  // Notifications
  notifications: string[];
  addNotification: (msg: string) => void;
  clearNotifications: () => void;
  // Global loading
  // Global loading
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
  // Active mission
  activeMission: string | null;
  setActiveMission: (mission: string | null) => void;
  // Real-time updates
  lastUpdate: number;
  bumpUpdate: () => void;
  // Chat Persist
  chatMessages: Message[];
  isChatLoading: boolean;
  setChatMessages: (updater: Message[] | ((prev: Message[]) => Message[])) => void;
  setChatLoading: (loading: boolean) => void;
}
export const useStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) =>
        set({
          user,
        }),
      theme: "system",
      setTheme: (theme) =>
        set({
          theme,
        }),
      sidebarOpen: true,
      toggleSidebar: () =>
        set((s) => ({
          sidebarOpen: !s.sidebarOpen,
        })),
      setSidebarOpen: (open) =>
        set({
          sidebarOpen: open,
        }),
      notifications: [],
      addNotification: (msg) =>
        set((s) => ({
          notifications: [...s.notifications.slice(-9), msg],
        })),
      clearNotifications: () =>
        set({
          notifications: [],
        }),
      isLoading: false,
      setLoading: (loading) =>
        set({
          isLoading: loading,
        }),
      activeMission: null,
      setActiveMission: (mission) =>
        set({
          activeMission: mission,
        }),
      lastUpdate: Date.now(),
      bumpUpdate: () =>
        set({
          lastUpdate: Date.now(),
        }),
      chatMessages: [],
      isChatLoading: false,
      setChatMessages: (updater) =>
        set((s) => ({
          chatMessages: typeof updater === "function" ? updater(s.chatMessages) : updater,
        })),
      setChatLoading: (loading) => set({ isChatLoading: loading }),
    }),
    {
      name: "sentience-store",
      partialize: (state) => ({
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
        user: state.user,
        chatMessages: state.chatMessages,
      }),
    },
  ),
);
