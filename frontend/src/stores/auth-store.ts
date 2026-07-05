import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/types";
import {
  setAuthTokens,
  clearAuthTokens,
  apiClient,
} from "@/lib/api/client";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  login: (email: string, password: string) => Promise<void>;
  register: (data: Record<string, string>) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) =>
        set({ user, isAuthenticated: !!user }),

      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const { data } = await apiClient.post("/auth/login/", {
            email,
            password,
          });
          setAuthTokens(data.access, data.refresh);
          set({ user: data.user, isAuthenticated: true });
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (formData) => {
        set({ isLoading: true });
        try {
          const { data } = await apiClient.post("/auth/register/", formData);
          setAuthTokens(data.access, data.refresh);
          set({ user: data.user, isAuthenticated: true });
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        clearAuthTokens();
        set({ user: null, isAuthenticated: false });
      },

      fetchUser: async () => {
        try {
          const { data } = await apiClient.get("/auth/me/");
          set({ user: data, isAuthenticated: true });
        } catch {
          set({ user: null, isAuthenticated: false });
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
