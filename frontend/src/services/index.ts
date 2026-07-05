import { apiClient } from "@/lib/api/client";
import type {
  PaginatedResponse,
  Product,
  ProductFilters,
  Category,
  Brand,
  Cart,
  Order,
  Address,
  BlogPost,
  Review,
  Coupon,
  Notification,
  Ticket,
  CMSPage,
  Wallet,
  User,
} from "@/types";

export const productService = {
  getAll: (filters?: ProductFilters) =>
    apiClient.get<PaginatedResponse<Product>>("/catalog/products/", {
      params: filters,
    }),

  getBySlug: (slug: string) =>
    apiClient.get<Product>(`/catalog/products/${slug}/`),

  getFeatured: () =>
    apiClient.get<Product[]>("/catalog/products/featured/"),

  getLatest: () =>
    apiClient.get<Product[]>("/catalog/products/latest/"),

  getPopular: () =>
    apiClient.get<Product[]>("/catalog/products/popular/"),

  getRelated: (slug: string) =>
    apiClient.get<Product[]>(`/catalog/products/${slug}/related/`),
};

export const categoryService = {
  getAll: () => apiClient.get<Category[]>("/catalog/categories/"),
  getBySlug: (slug: string) =>
    apiClient.get<Category>(`/catalog/categories/${slug}/`),
};

export const brandService = {
  getAll: () => apiClient.get<Brand[]>("/catalog/brands/"),
};

export const cartService = {
  get: () => apiClient.get<Cart>("/cart/"),
  addItem: (productId: number, quantity: number, variantId?: number) =>
    apiClient.post("/cart/items/", {
      product_id: productId,
      quantity,
      variant_id: variantId,
    }),
  updateItem: (itemId: number, quantity: number) =>
    apiClient.patch(`/cart/items/${itemId}/`, { quantity }),
  removeItem: (itemId: number) =>
    apiClient.delete(`/cart/items/${itemId}/`),
  applyCoupon: (code: string) =>
    apiClient.post("/cart/coupon/", { code }),
  clear: () => apiClient.delete("/cart/"),
};

export const orderService = {
  getAll: () => apiClient.get<PaginatedResponse<Order>>("/orders/"),
  getById: (id: number) => apiClient.get<Order>(`/orders/${id}/`),
  create: (data: Record<string, unknown>) =>
    apiClient.post<Order>("/orders/", data),
  cancel: (id: number) =>
    apiClient.post(`/orders/${id}/cancel/`),
};

export const addressService = {
  getAll: () => apiClient.get<Address[]>("/accounts/addresses/"),
  create: (data: Partial<Address>) =>
    apiClient.post<Address>("/accounts/addresses/", data),
  update: (id: number, data: Partial<Address>) =>
    apiClient.patch<Address>(`/accounts/addresses/${id}/`, data),
  delete: (id: number) =>
    apiClient.delete(`/accounts/addresses/${id}/`),
  setDefault: (id: number) =>
    apiClient.post(`/accounts/addresses/${id}/default/`),
};

export const authService = {
  login: (email: string, password: string) =>
    apiClient.post("/auth/login/", { email, password }),
  register: (data: Record<string, string>) =>
    apiClient.post("/auth/register/", data),
  forgotPassword: (email: string) =>
    apiClient.post("/auth/forgot-password/", { email }),
  resetPassword: (token: string, password: string) =>
    apiClient.post("/auth/reset-password/", { token, password }),
  getProfile: () => apiClient.get<User>("/auth/me/"),
  updateProfile: (data: Partial<User>) =>
    apiClient.patch<User>("/auth/me/", data),
  changePassword: (oldPassword: string, newPassword: string) =>
    apiClient.post("/auth/change-password/", {
      old_password: oldPassword,
      new_password: newPassword,
    }),
};

export const blogService = {
  getAll: (page?: number) =>
    apiClient.get<PaginatedResponse<BlogPost>>("/blog/posts/", {
      params: { page },
    }),
  getBySlug: (slug: string) =>
    apiClient.get<BlogPost>(`/blog/posts/${slug}/`),
};

export const reviewService = {
  getForProduct: (slug: string) =>
    apiClient.get<Review[]>(`/reviews/products/${slug}/`),
  create: (productId: number, data: { rating: number; title: string; comment: string }) =>
    apiClient.post("/reviews/", { product_id: productId, ...data }),
  getUserReviews: () => apiClient.get<Review[]>("/reviews/me/"),
};

export const searchService = {
  search: (query: string, filters?: ProductFilters) =>
    apiClient.get<PaginatedResponse<Product>>("/search/", {
      params: { q: query, ...filters },
    }),
};

export const couponService = {
  getUserCoupons: () => apiClient.get<Coupon[]>("/promotions/coupons/me/"),
  validate: (code: string) =>
    apiClient.post<Coupon>("/promotions/coupons/validate/", { code }),
};

export const notificationService = {
  getAll: () => apiClient.get<Notification[]>("/notifications/"),
  markRead: (id: number) =>
    apiClient.post(`/notifications/${id}/read/`),
  markAllRead: () => apiClient.post("/notifications/read-all/"),
};

export const ticketService = {
  getAll: () => apiClient.get<Ticket[]>("/support/tickets/"),
  getById: (id: number) => apiClient.get<Ticket>(`/support/tickets/${id}/`),
  create: (data: { subject: string; category: string; message: string; priority: string }) =>
    apiClient.post<Ticket>("/support/tickets/", data),
  reply: (id: number, message: string) =>
    apiClient.post(`/support/tickets/${id}/reply/`, { message }),
};

export const cmsService = {
  getPage: (slug: string) =>
    apiClient.get<CMSPage>(`/cms/pages/${slug}/`),
};

export const walletService = {
  get: () => apiClient.get<Wallet>("/payments/wallet/"),
  topUp: (amount: number) =>
    apiClient.post("/payments/wallet/top-up/", { amount }),
};

export const contactService = {
  send: (data: { name: string; email: string; subject: string; message: string }) =>
    apiClient.post("/support/contact/", data),
};
