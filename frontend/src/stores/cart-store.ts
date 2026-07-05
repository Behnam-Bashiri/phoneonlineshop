import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product, ProductVariant } from "@/types";

export interface LocalCartItem {
  product: Product;
  variant?: ProductVariant;
  quantity: number;
}

interface CartState {
  items: LocalCartItem[];
  couponCode: string | null;
  addItem: (product: Product, variant?: ProductVariant, quantity?: number) => void;
  removeItem: (productId: number, variantId?: number) => void;
  updateQuantity: (productId: number, quantity: number, variantId?: number) => void;
  clearCart: () => void;
  setCoupon: (code: string | null) => void;
  getItemCount: () => number;
  getSubtotal: () => number;
}

function itemKey(productId: number, variantId?: number) {
  return `${productId}-${variantId ?? "default"}`;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      couponCode: null,

      addItem: (product, variant, quantity = 1) => {
        set((state) => {
          const key = itemKey(product.id, variant?.id);
          const existing = state.items.find(
            (i) => itemKey(i.product.id, i.variant?.id) === key
          );
          if (existing) {
            return {
              items: state.items.map((i) =>
                itemKey(i.product.id, i.variant?.id) === key
                  ? { ...i, quantity: i.quantity + quantity }
                  : i
              ),
            };
          }
          return { items: [...state.items, { product, variant, quantity }] };
        });
      },

      removeItem: (productId, variantId) => {
        const key = itemKey(productId, variantId);
        set((state) => ({
          items: state.items.filter(
            (i) => itemKey(i.product.id, i.variant?.id) !== key
          ),
        }));
      },

      updateQuantity: (productId, quantity, variantId) => {
        const key = itemKey(productId, variantId);
        if (quantity <= 0) {
          get().removeItem(productId, variantId);
          return;
        }
        set((state) => ({
          items: state.items.map((i) =>
            itemKey(i.product.id, i.variant?.id) === key
              ? { ...i, quantity }
              : i
          ),
        }));
      },

      clearCart: () => set({ items: [], couponCode: null }),

      setCoupon: (code) => set({ couponCode: code }),

      getItemCount: () =>
        get().items.reduce((sum, item) => sum + item.quantity, 0),

      getSubtotal: () =>
        get().items.reduce((sum, item) => {
          const price = item.variant?.price ?? item.product.price;
          return sum + price * item.quantity;
        }, 0),
    }),
    { name: "cart-storage" }
  )
);
