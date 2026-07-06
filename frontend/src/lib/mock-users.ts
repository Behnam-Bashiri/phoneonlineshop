import type { Locale } from "@/lib/i18n";
import type {
  Address,
  Coupon,
  Notification,
  Order,
  Ticket,
  User,
  WalletTransaction,
} from "@/types";

export interface MockUserCredentials {
  email: string;
  password: string;
}

export interface MockUserProfile extends User {
  role: "admin" | "customer";
  is_staff: boolean;
  preferred_language: Locale;
}

export interface MockAuthResponse {
  user: MockUserProfile;
  tokens: { access: string; refresh: string };
}

export interface MockUserAccountData {
  orders: Order[];
  addresses: Address[];
  walletBalance: number;
  walletTransactions: WalletTransaction[];
  notifications: Notification[];
  tickets: Ticket[];
  coupons: Coupon[];
  reviews: Array<{
    id: number;
    productName: string;
    rating: number;
    title: string;
    comment: string;
    created_at: string;
  }>;
  club: {
    tier: string;
    tierFa: string;
    points: number;
    nextTier: string;
    nextTierFa: string;
    nextTierPoints: number;
  };
}

const MOCK_CREDENTIALS: MockUserCredentials[] = [
  { email: "admin@phonyshop.com", password: "admin123" },
  { email: "customer@phonyshop.com", password: "customer123" },
];

export const MOCK_USER_HINTS = {
  admin: { email: "admin@phonyshop.com", password: "admin123" },
  customer: { email: "customer@phonyshop.com", password: "customer123" },
} as const;

const usersEn: Record<string, MockUserProfile> = {
  "admin@phonyshop.com": {
    id: 1,
    email: "admin@phonyshop.com",
    first_name: "Admin",
    last_name: "User",
    phone: "+982112345678",
    is_verified: true,
    date_joined: "2024-01-01T00:00:00Z",
    role: "admin",
    is_staff: true,
    preferred_language: "en",
    bio: "PhonyShop platform administrator",
  },
  "customer@phonyshop.com": {
    id: 2,
    email: "customer@phonyshop.com",
    first_name: "Ali",
    last_name: "Rezaei",
    phone: "+989121234567",
    is_verified: true,
    date_joined: "2024-06-15T00:00:00Z",
    role: "customer",
    is_staff: false,
    preferred_language: "en",
    bio: "Premium smartphone enthusiast",
  },
};

const usersFa: Record<string, MockUserProfile> = {
  "admin@phonyshop.com": {
    ...usersEn["admin@phonyshop.com"],
    first_name: "مدیر",
    last_name: "سیستم",
    preferred_language: "fa",
    bio: "مدیر پلتفرم فونی‌شاپ",
  },
  "customer@phonyshop.com": {
    ...usersEn["customer@phonyshop.com"],
    first_name: "علی",
    last_name: "رضایی",
    preferred_language: "fa",
    bio: "علاقه‌مند به گوشی‌های پریمیوم",
  },
};

function accountDataEn(email: string): MockUserAccountData | null {
  if (email === "admin@phonyshop.com") {
    return {
      orders: [],
      addresses: [],
      walletBalance: 0,
      walletTransactions: [],
      notifications: [
        {
          id: 1,
          title: "New order received",
          message: "Order PS-20250610 placed by a customer.",
          type: "info",
          is_read: false,
          created_at: "2025-06-10T08:00:00Z",
          link: "/account/orders",
        },
        {
          id: 2,
          title: "Low stock alert",
          message: "iPhone 16 Pro Max stock is below reorder level.",
          type: "warning",
          is_read: true,
          created_at: "2025-06-09T14:30:00Z",
        },
      ],
      tickets: [],
      coupons: [],
      reviews: [],
      club: {
        tier: "Admin",
        tierFa: "مدیر",
        points: 0,
        nextTier: "—",
        nextTierFa: "—",
        nextTierPoints: 0,
      },
    };
  }

  if (email === "customer@phonyshop.com") {
    return {
      orders: [
        {
          id: 1,
          order_number: "PS-20250601",
          status: "delivered",
          items: [],
          subtotal: 1199,
          discount: 100,
          shipping: 0,
          total: 1099,
          address: {
            id: 1,
            title: "Home",
            full_name: "Ali Rezaei",
            phone: "+989121234567",
            province: "Tehran",
            city: "Tehran",
            address: "Valiasr St, No. 123",
            postal_code: "1969712345",
            is_default: true,
          },
          payment_method: "Online",
          tracking_number: "TRK-8849201",
          created_at: "2025-06-01T10:30:00Z",
          updated_at: "2025-06-05T16:00:00Z",
        },
        {
          id: 2,
          order_number: "PS-20250515",
          status: "shipped",
          items: [],
          subtotal: 249,
          discount: 0,
          shipping: 10,
          total: 259,
          address: {
            id: 1,
            title: "Home",
            full_name: "Ali Rezaei",
            phone: "+989121234567",
            province: "Tehran",
            city: "Tehran",
            address: "Valiasr St, No. 123",
            postal_code: "1969712345",
            is_default: true,
          },
          payment_method: "Wallet",
          tracking_number: "TRK-7723104",
          created_at: "2025-05-15T14:00:00Z",
          updated_at: "2025-05-17T09:00:00Z",
        },
        {
          id: 3,
          order_number: "PS-20250420",
          status: "processing",
          items: [],
          subtotal: 1099,
          discount: 50,
          shipping: 0,
          total: 1049,
          address: {
            id: 2,
            title: "Office",
            full_name: "Ali Rezaei",
            phone: "+989121234567",
            province: "Tehran",
            city: "Tehran",
            address: "Jordan St, Tower B, Floor 5",
            postal_code: "1965843210",
            is_default: false,
          },
          payment_method: "Online",
          created_at: "2025-04-20T11:15:00Z",
          updated_at: "2025-04-20T11:15:00Z",
        },
      ],
      addresses: [
        {
          id: 1,
          title: "Home",
          full_name: "Ali Rezaei",
          phone: "+989121234567",
          province: "Tehran",
          city: "Tehran",
          address: "Valiasr St, No. 123, Unit 4",
          postal_code: "1969712345",
          is_default: true,
        },
        {
          id: 2,
          title: "Office",
          full_name: "Ali Rezaei",
          phone: "+989121234567",
          province: "Tehran",
          city: "Tehran",
          address: "Jordan St, Tower B, Floor 5",
          postal_code: "1965843210",
          is_default: false,
        },
      ],
      walletBalance: 12500000,
      walletTransactions: [
        {
          id: 1,
          amount: 5000000,
          type: "credit",
          description: "Wallet top up",
          created_at: "2025-06-01T09:00:00Z",
        },
        {
          id: 2,
          amount: 10990000,
          type: "debit",
          description: "Order PS-20250601",
          created_at: "2025-06-01T10:35:00Z",
        },
        {
          id: 3,
          amount: 2500000,
          type: "credit",
          description: "Cashback reward",
          created_at: "2025-05-28T12:00:00Z",
        },
        {
          id: 4,
          amount: 2590000,
          type: "debit",
          description: "Order PS-20250515",
          created_at: "2025-05-15T14:05:00Z",
        },
        {
          id: 5,
          amount: 1000000,
          type: "credit",
          description: "Referral bonus",
          created_at: "2025-05-10T08:00:00Z",
        },
      ],
      notifications: [
        {
          id: 1,
          title: "Order delivered",
          message: "Your order PS-20250601 has been delivered successfully.",
          type: "success",
          is_read: false,
          created_at: "2025-06-05T16:00:00Z",
          link: "/account/orders",
        },
        {
          id: 2,
          title: "Order shipped",
          message: "Order PS-20250515 is on its way. Tracking: TRK-7723104",
          type: "info",
          is_read: true,
          created_at: "2025-05-17T09:00:00Z",
        },
        {
          id: 3,
          title: "New coupon available",
          message: "You received a 15% off coupon for your next purchase.",
          type: "success",
          is_read: false,
          created_at: "2025-05-20T10:00:00Z",
          link: "/account/coupons",
        },
      ],
      tickets: [
        {
          id: 1,
          subject: "Warranty question for iPhone 16",
          category: "Warranty",
          status: "resolved",
          priority: "medium",
          messages: [
            {
              id: 1,
              message: "How long is the warranty for iPhone 16 Pro Max?",
              is_staff: false,
              created_at: "2025-05-10T10:00:00Z",
            },
            {
              id: 2,
              message:
                "Apple provides 1 year manufacturer warranty. We offer an additional 1 year extended warranty.",
              is_staff: true,
              created_at: "2025-05-10T14:30:00Z",
            },
          ],
          created_at: "2025-05-10T10:00:00Z",
          updated_at: "2025-05-10T14:30:00Z",
        },
        {
          id: 2,
          subject: "Delivery delay",
          category: "Shipping",
          status: "in_progress",
          priority: "high",
          messages: [
            {
              id: 3,
              message: "My order PS-20250515 hasn't arrived yet.",
              is_staff: false,
              created_at: "2025-05-20T09:00:00Z",
            },
          ],
          created_at: "2025-05-20T09:00:00Z",
          updated_at: "2025-05-20T09:00:00Z",
        },
      ],
      coupons: [
        {
          id: 1,
          code: "WELCOME15",
          discount_type: "percentage",
          discount_value: 15,
          min_order: 500,
          expires_at: "2025-12-31T23:59:59Z",
          is_active: true,
        },
        {
          id: 2,
          code: "SUMMER50",
          discount_type: "fixed",
          discount_value: 50,
          min_order: 200,
          expires_at: "2025-08-31T23:59:59Z",
          is_active: true,
        },
      ],
      reviews: [
        {
          id: 1,
          productName: "iPhone 16 Pro Max",
          rating: 5,
          title: "Best phone ever",
          comment: "Amazing camera and build quality. Highly recommended!",
          created_at: "2025-06-02T00:00:00Z",
        },
        {
          id: 2,
          productName: "AirPods Pro 3",
          rating: 4,
          title: "Great ANC",
          comment: "Noise cancellation is excellent. Battery could be better.",
          created_at: "2025-05-18T00:00:00Z",
        },
      ],
      club: {
        tier: "Gold",
        tierFa: "طلایی",
        points: 2450,
        nextTier: "Platinum",
        nextTierFa: "پلاتینیوم",
        nextTierPoints: 3000,
      },
    };
  }

  return null;
}

function accountDataFa(email: string): MockUserAccountData | null {
  const base = accountDataEn(email);
  if (!base) return null;

  if (email === "admin@phonyshop.com") {
    return {
      ...base,
      notifications: base.notifications.map((n) => ({
        ...n,
        title: n.id === 1 ? "سفارش جدید دریافت شد" : "هشدار کمبود موجودی",
        message:
          n.id === 1
            ? "سفارش PS-20250610 توسط یک مشتری ثبت شد."
            : "موجودی آیفون ۱۶ پرو مکس زیر حد مجاز است.",
      })),
    };
  }

  return {
    ...base,
    orders: base.orders.map((o) => ({
      ...o,
      address: {
        ...o.address,
        title: o.address.title === "Home" ? "منزل" : "محل کار",
        full_name: "علی رضایی",
        province: "تهران",
        city: "تهران",
        address:
          o.address.id === 1
            ? "خیابان ولیعصر، پلاک ۱۲۳، واحد ۴"
            : "خیابان جردن، برج B، طبقه ۵",
      },
      payment_method: o.payment_method === "Online" ? "آنلاین" : "کیف پول",
    })),
    addresses: base.addresses.map((a) => ({
      ...a,
      title: a.title === "Home" ? "منزل" : "محل کار",
      full_name: "علی رضایی",
      province: "تهران",
      city: "تهران",
      address:
        a.id === 1
          ? "خیابان ولیعصر، پلاک ۱۲۳، واحد ۴"
          : "خیابان جردن، برج B، طبقه ۵",
    })),
    walletTransactions: base.walletTransactions.map((tx) => ({
      ...tx,
      description:
        tx.id === 1
          ? "شارژ کیف پول"
          : tx.id === 2
            ? "سفارش PS-20250601"
            : tx.id === 3
              ? "پاداش کش‌بک"
              : tx.id === 4
                ? "سفارش PS-20250515"
                : "پاداش معرفی",
    })),
    notifications: base.notifications.map((n) => ({
      ...n,
      title:
        n.id === 1
          ? "تحویل سفارش"
          : n.id === 2
            ? "ارسال سفارش"
            : "کد تخفیف جدید",
      message:
        n.id === 1
          ? "سفارش PS-20250601 با موفقیت تحویل داده شد."
          : n.id === 2
            ? "سفارش PS-20250515 در راه است. کد پیگیری: TRK-7723104"
            : "کد تخفیف ۱۵٪ برای خرید بعدی شما فعال شد.",
    })),
    tickets: base.tickets.map((t) => ({
      ...t,
      subject: t.id === 1 ? "سوال گارانتی آیفون ۱۶" : "تأخیر در تحویل",
      category: t.id === 1 ? "گارانتی" : "ارسال",
      messages: t.messages.map((m) => ({
        ...m,
        message:
          m.id === 1
            ? "گارانتی آیفون ۱۶ پرو مکس چند سال است؟"
            : m.id === 2
              ? "اپل ۱ سال گارانتی کارخانه دارد. ما ۱ سال گارانتی تمدیدی هم ارائه می‌دهیم."
              : "سفارش PS-20250515 هنوز نرسیده است.",
      })),
    })),
    reviews: base.reviews.map((r) => ({
      ...r,
      productName: r.id === 1 ? "آیفون ۱۶ پرو مکس" : "ایرپادز پرو ۳",
      title: r.id === 1 ? "بهترین گوشی" : "ANC عالی",
      comment:
        r.id === 1
          ? "دوربین و کیفیت ساخت فوق‌العاده است. پیشنهاد می‌کنم!"
          : "حذف نویز عالی است. باتری می‌توانست بهتر باشد.",
    })),
  };
}

export function authenticateMockUser(
  email: string,
  password: string,
  locale: Locale = "en"
): MockAuthResponse | null {
  const valid = MOCK_CREDENTIALS.find(
    (c) => c.email === email && c.password === password
  );
  if (!valid) return null;

  const users = locale === "fa" ? usersFa : usersEn;
  const user = users[email];
  if (!user) return null;

  return {
    user,
    tokens: {
      access: `mock-access-${user.role}-${user.id}`,
      refresh: `mock-refresh-${user.role}-${user.id}`,
    },
  };
}

export function getMockUserAccountData(
  locale: Locale,
  email?: string | null
): MockUserAccountData | null {
  if (!email) return null;
  return locale === "fa" ? accountDataFa(email) : accountDataEn(email);
}

export function isMockToken(token: string | null): boolean {
  return Boolean(token?.startsWith("mock-access-"));
}

export function getWalletDisplayAmount(amount: number, locale: Locale): number {
  if (locale === "fa") return amount;
  return amount / 50000;
}
