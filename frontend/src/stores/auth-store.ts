import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/types";
import type { Locale } from "@/lib/i18n";
import {
  authenticateMockUser,
  isMockToken,
} from "@/lib/mock-users";
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
  login: (email: string, password: string, locale?: Locale) => Promise<void>;
  register: (data: Record<string, string>) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

function getLocaleFromPath(): Locale {
  if (typeof window === "undefined") return "en";
  const seg = window.location.pathname.split("/")[1];
  return seg === "fa" ? "fa" : "en";
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) =>
        set({ user, isAuthenticated: !!user }),

      login: async (email, password, locale) => {
        const loc = locale ?? getLocaleFromPath();
        set({ isLoading: true });
        try {
          const { data } = await apiClient.post("/auth/login/", {
            email,
            password,
          });
          setAuthTokens(data.access, data.refresh);
          set({ user: data.user, isAuthenticated: true });
        } catch {
          const mockAuth = authenticateMockUser(email, password, loc);
          if (mockAuth) {
            setAuthTokens(mockAuth.tokens.access, mockAuth.tokens.refresh);
            set({ user: mockAuth.user, isAuthenticated: true });
            return;
          }
          throw new Error(
            loc === "fa"
              ? "ایمیل یا رمز عبور اشتباه است"
              : "Invalid email or password"
          );
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
        const token =
          typeof window !== "undefined"
            ? localStorage.getItem("access_token")
            : null;

        if (isMockToken(token)) {
          const { user } = get();
          if (user) {
            set({ isAuthenticated: true });
            return;
          }
        }

        try {
          const { data } = await apiClient.get("/auth/me/");
          set({ user: data, isAuthenticated: true });
        } catch {
          if (!isMockToken(token)) {
            set({ user: null, isAuthenticated: false });
          }
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
