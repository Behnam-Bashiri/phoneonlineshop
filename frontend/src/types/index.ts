export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar?: string;
  bio?: string;
  is_verified: boolean;
  date_joined: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  image?: string;
  parent?: number;
  children?: Category[];
  product_count?: number;
}

export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo?: string;
  description?: string;
}

export interface ProductImage {
  id: number;
  image: string;
  alt?: string;
  is_primary: boolean;
}

export interface ProductVariant {
  id: number;
  name: string;
  sku: string;
  price: number;
  compare_at_price?: number;
  stock: number;
  attributes: Record<string, string>;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description?: string;
  price: number;
  compare_at_price?: number;
  discount_percent?: number;
  sku: string;
  stock: number;
  is_featured: boolean;
  is_new: boolean;
  rating: number;
  review_count: number;
  images: ProductImage[];
  category: Category;
  brand?: Brand;
  variants?: ProductVariant[];
  specifications?: Record<string, string>;
  tags?: string[];
  created_at: string;
}

export interface CartItem {
  id: number;
  product: Product;
  variant?: ProductVariant;
  quantity: number;
  price: number;
  total: number;
}

export interface Cart {
  id: number;
  items: CartItem[];
  subtotal: number;
  discount: number;
  shipping: number;
  total: number;
  item_count: number;
}

export interface Address {
  id: number;
  title: string;
  full_name: string;
  phone: string;
  province: string;
  city: string;
  address: string;
  postal_code: string;
  is_default: boolean;
}

export interface OrderItem {
  id: number;
  product: Product;
  quantity: number;
  price: number;
  total: number;
}

export interface Order {
  id: number;
  order_number: string;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  items: OrderItem[];
  subtotal: number;
  discount: number;
  shipping: number;
  total: number;
  address: Address;
  payment_method: string;
  tracking_number?: string;
  created_at: string;
  updated_at: string;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  image?: string;
  author: { name: string; avatar?: string };
  category: string;
  tags: string[];
  published_at: string;
  read_time: number;
}

export interface Review {
  id: number;
  user: { name: string; avatar?: string };
  product: Product;
  rating: number;
  title: string;
  comment: string;
  created_at: string;
  is_verified: boolean;
}

export interface Coupon {
  id: number;
  code: string;
  discount_type: "percentage" | "fixed";
  discount_value: number;
  min_order: number;
  expires_at: string;
  is_active: boolean;
}

export interface Notification {
  id: number;
  title: string;
  message: string;
  type: "info" | "success" | "warning" | "error";
  is_read: boolean;
  created_at: string;
  link?: string;
}

export interface Ticket {
  id: number;
  subject: string;
  category: string;
  status: "open" | "in_progress" | "resolved" | "closed";
  priority: "low" | "medium" | "high";
  messages: TicketMessage[];
  created_at: string;
  updated_at: string;
}

export interface TicketMessage {
  id: number;
  message: string;
  is_staff: boolean;
  created_at: string;
  attachments?: string[];
}

export interface CMSPage {
  id: number;
  title: string;
  slug: string;
  content: string;
  meta_title?: string;
  meta_description?: string;
}

export interface Wallet {
  balance: number;
  currency: string;
  transactions: WalletTransaction[];
}

export interface WalletTransaction {
  id: number;
  amount: number;
  type: "credit" | "debit";
  description: string;
  created_at: string;
}

export interface ProductFilters {
  category?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  sort?: string;
  search?: string;
  page?: number;
  page_size?: number;
  is_featured?: boolean;
  is_new?: boolean;
}

export interface HeroSlide {
  id: number;
  title: string;
  subtitle: string;
  image: string;
  link: string;
  button_text: string;
}

export interface FAQ {
  id: number;
  question: string;
  answer: string;
  category: string;
}

export interface Partner {
  id: number;
  name: string;
  logo: string;
  url?: string;
}

export interface Stat {
  label: string;
  value: string;
  icon: string;
}

export interface Advantage {
  id: number;
  title: string;
  description: string;
  icon: string;
}

export interface Offer {
  id: number;
  title: string;
  description: string;
  image: string;
  discount: number;
  end_date: string;
  link: string;
}
