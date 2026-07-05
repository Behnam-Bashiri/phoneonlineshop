import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "@/types";

const MAX_COMPARE = 4;

interface CompareState {
  items: Product[];
  addItem: (product: Product) => void;
  removeItem: (productId: number) => void;
  clearAll: () => void;
  isInCompare: (productId: number) => boolean;
}

export const useCompareStore = create<CompareState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product) =>
        set((state) => {
          if (state.items.some((i) => i.id === product.id)) return state;
          if (state.items.length >= MAX_COMPARE) return state;
          return { items: [...state.items, product] };
        }),

      removeItem: (productId) =>
        set((state) => ({
          items: state.items.filter((i) => i.id !== productId),
        })),

      clearAll: () => set({ items: [] }),

      isInCompare: (productId) =>
        get().items.some((i) => i.id === productId),
    }),
    { name: "compare-storage" }
  )
);
