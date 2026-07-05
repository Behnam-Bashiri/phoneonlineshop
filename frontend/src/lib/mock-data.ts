import type {
  Product,
  Category,
  Brand,
  BlogPost,
  Review,
  HeroSlide,
  FAQ,
  Partner,
  Offer,
  Advantage,
} from "@/types";

export const mockProducts: Product[] = [
  {
    id: 1,
    name: "iPhone 16 Pro Max",
    slug: "iphone-16-pro-max",
    description:
      "The most advanced iPhone ever with A18 Pro chip, titanium design, and revolutionary camera system.",
    short_description: "Titanium. A18 Pro. Camera Control.",
    price: 1199,
    compare_at_price: 1299,
    discount_percent: 8,
    sku: "IP16PM-256",
    stock: 45,
    is_featured: true,
    is_new: true,
    rating: 4.9,
    review_count: 128,
    images: [
      {
        id: 1,
        image: "https://images.unsplash.com/photo-1695048133142-1a204686a853?w=800",
        alt: "iPhone 16 Pro Max",
        is_primary: true,
      },
    ],
    category: { id: 1, name: "Smartphones", slug: "smartphones" },
    brand: { id: 1, name: "Apple", slug: "apple" },
    specifications: {
      Display: "6.9-inch Super Retina XDR",
      Chip: "A18 Pro",
      Storage: "256GB",
      Camera: "48MP Main + 48MP Ultra Wide",
      Battery: "Up to 29 hours video playback",
    },
    tags: ["flagship", "5g", "titanium"],
    created_at: "2025-09-15T00:00:00Z",
  },
  {
    id: 2,
    name: "Samsung Galaxy S25 Ultra",
    slug: "samsung-galaxy-s25-ultra",
    description:
      "Galaxy AI meets premium design with S Pen, 200MP camera, and Snapdragon 8 Elite.",
    short_description: "Galaxy AI. S Pen included.",
    price: 1099,
    compare_at_price: 1199,
    discount_percent: 8,
    sku: "SGS25U-512",
    stock: 32,
    is_featured: true,
    is_new: true,
    rating: 4.8,
    review_count: 95,
    images: [
      {
        id: 2,
        image: "https://images.unsplash.com/photo-1610945265064-0e34e5519dff?w=800",
        alt: "Samsung Galaxy S25 Ultra",
        is_primary: true,
      },
    ],
    category: { id: 1, name: "Smartphones", slug: "smartphones" },
    brand: { id: 2, name: "Samsung", slug: "samsung" },
    specifications: {
      Display: "6.8-inch Dynamic AMOLED 2X",
      Chip: "Snapdragon 8 Elite",
      Storage: "512GB",
      Camera: "200MP Main",
      Battery: "5000mAh",
    },
    tags: ["flagship", "s-pen", "ai"],
    created_at: "2025-01-20T00:00:00Z",
  },
  {
    id: 3,
    name: "Google Pixel 9 Pro",
    slug: "google-pixel-9-pro",
    description:
      "The best of Google AI in a stunning design with unmatched computational photography.",
    short_description: "Best of Google AI.",
    price: 999,
    sku: "GP9P-256",
    stock: 28,
    is_featured: false,
    is_new: true,
    rating: 4.7,
    review_count: 67,
    images: [
      {
        id: 3,
        image: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800",
        alt: "Google Pixel 9 Pro",
        is_primary: true,
      },
    ],
    category: { id: 1, name: "Smartphones", slug: "smartphones" },
    brand: { id: 3, name: "Google", slug: "google" },
    tags: ["ai", "photography"],
    created_at: "2025-02-01T00:00:00Z",
  },
  {
    id: 4,
    name: "OnePlus 13",
    slug: "oneplus-13",
    description: "Never Settle with flagship performance at a competitive price.",
    short_description: "Flagship killer performance.",
    price: 799,
    compare_at_price: 899,
    discount_percent: 11,
    sku: "OP13-256",
    stock: 55,
    is_featured: true,
    is_new: false,
    rating: 4.6,
    review_count: 84,
    images: [
      {
        id: 4,
        image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
        alt: "OnePlus 13",
        is_primary: true,
      },
    ],
    category: { id: 1, name: "Smartphones", slug: "smartphones" },
    brand: { id: 4, name: "OnePlus", slug: "oneplus" },
    tags: ["value", "fast-charging"],
    created_at: "2024-11-10T00:00:00Z",
  },
  {
    id: 5,
    name: "Xiaomi 15 Ultra",
    slug: "xiaomi-15-ultra",
    description: "Leica optics meet Snapdragon power in this photography powerhouse.",
    short_description: "Leica camera system.",
    price: 899,
    sku: "XM15U-512",
    stock: 40,
    is_featured: false,
    is_new: true,
    rating: 4.5,
    review_count: 52,
    images: [
      {
        id: 5,
        image: "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=800",
        alt: "Xiaomi 15 Ultra",
        is_primary: true,
      },
    ],
    category: { id: 1, name: "Smartphones", slug: "smartphones" },
    brand: { id: 5, name: "Xiaomi", slug: "xiaomi" },
    tags: ["leica", "photography"],
    created_at: "2025-03-01T00:00:00Z",
  },
  {
    id: 6,
    name: "AirPods Pro 3",
    slug: "airpods-pro-3",
    description: "Active Noise Cancellation redefined with Adaptive Audio and USB-C.",
    short_description: "Next-gen ANC earbuds.",
    price: 249,
    sku: "APP3-WHT",
    stock: 120,
    is_featured: true,
    is_new: true,
    rating: 4.8,
    review_count: 210,
    images: [
      {
        id: 6,
        image: "https://images.unsplash.com/photo-1606841837239-b5d59190402e?w=800",
        alt: "AirPods Pro 3",
        is_primary: true,
      },
    ],
    category: { id: 2, name: "Accessories", slug: "accessories" },
    brand: { id: 1, name: "Apple", slug: "apple" },
    tags: ["earbuds", "anc"],
    created_at: "2025-01-05T00:00:00Z",
  },
];

export const mockCategories: Category[] = [
  { id: 1, name: "Smartphones", slug: "smartphones", product_count: 156 },
  { id: 2, name: "Accessories", slug: "accessories", product_count: 342 },
  { id: 3, name: "Tablets", slug: "tablets", product_count: 48 },
  { id: 4, name: "Wearables", slug: "wearables", product_count: 89 },
  { id: 5, name: "Cases", slug: "cases", product_count: 520 },
  { id: 6, name: "Chargers", slug: "chargers", product_count: 178 },
];

export const mockBrands: Brand[] = [
  { id: 1, name: "Apple", slug: "apple", logo: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" },
  { id: 2, name: "Samsung", slug: "samsung" },
  { id: 3, name: "Google", slug: "google" },
  { id: 4, name: "OnePlus", slug: "oneplus" },
  { id: 5, name: "Xiaomi", slug: "xiaomi" },
  { id: 6, name: "Sony", slug: "sony" },
];

export const mockHeroSlides: HeroSlide[] = [
  {
    id: 1,
    title: "iPhone 16 Pro Max",
    subtitle: "Titanium. So strong. So light. So Pro.",
    image: "https://images.unsplash.com/photo-1695048133142-1a204686a853?w=1600",
    link: "/products/iphone-16-pro-max",
    button_text: "Shop Now",
  },
  {
    id: 2,
    title: "Galaxy S25 Ultra",
    subtitle: "Galaxy AI is here. Experience the future.",
    image: "https://images.unsplash.com/photo-1610945265064-0e34e5519dff?w=1600",
    link: "/products/samsung-galaxy-s25-ultra",
    button_text: "Explore",
  },
  {
    id: 3,
    title: "Summer Sale",
    subtitle: "Up to 30% off on selected devices",
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1600",
    link: "/products?sort=discount",
    button_text: "View Deals",
  },
];

export const mockReviews: Review[] = [
  {
    id: 1,
    user: { name: "Sarah M.", avatar: "" },
    product: mockProducts[0],
    rating: 5,
    title: "Best phone I've ever owned",
    comment: "The camera quality is incredible and the titanium build feels premium.",
    created_at: "2025-06-01T00:00:00Z",
    is_verified: true,
  },
  {
    id: 2,
    user: { name: "Ali R.", avatar: "" },
    product: mockProducts[1],
    rating: 5,
    title: "Galaxy AI is a game changer",
    comment: "The S Pen and AI features make this the most productive phone ever.",
    created_at: "2025-05-28T00:00:00Z",
    is_verified: true,
  },
  {
    id: 3,
    user: { name: "John D.", avatar: "" },
    product: mockProducts[2],
    rating: 4,
    title: "Great camera, smooth software",
    comment: "Pixel photos are unmatched. Battery could be better though.",
    created_at: "2025-05-20T00:00:00Z",
    is_verified: true,
  },
];

export const mockBlogPosts: BlogPost[] = [
  {
    id: 1,
    title: "iPhone 16 vs Samsung S25: Which Flagship Wins?",
    slug: "iphone-16-vs-samsung-s25",
    excerpt: "We compare the two biggest flagships of 2025 head to head.",
    content: "Full comparison article content...",
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
    author: { name: "Tech Team" },
    category: "Reviews",
    tags: ["comparison", "flagship"],
    published_at: "2025-06-01T00:00:00Z",
    read_time: 8,
  },
  {
    id: 2,
    title: "Best Budget Phones Under $500 in 2025",
    slug: "best-budget-phones-2025",
    excerpt: "Premium features without the premium price tag.",
    content: "Full article content...",
    image: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800",
    author: { name: "Buying Guide" },
    category: "Guides",
    tags: ["budget", "guide"],
    published_at: "2025-05-25T00:00:00Z",
    read_time: 6,
  },
  {
    id: 3,
    title: "How to Choose the Right Phone Case",
    slug: "choose-phone-case",
    excerpt: "Protection vs style — find your perfect match.",
    content: "Full article content...",
    image: "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800",
    author: { name: "Accessories" },
    category: "Tips",
    tags: ["accessories", "cases"],
    published_at: "2025-05-15T00:00:00Z",
    read_time: 4,
  },
];

export const mockFAQs: FAQ[] = [
  {
    id: 1,
    question: "What is your return policy?",
    answer: "We offer a 30-day hassle-free return policy on all products. Items must be in original condition with all accessories included.",
    category: "Returns",
  },
  {
    id: 2,
    question: "Do you offer international shipping?",
    answer: "Yes, we ship to over 50 countries worldwide. Shipping costs and delivery times vary by destination.",
    category: "Shipping",
  },
  {
    id: 3,
    question: "Are all products genuine?",
    answer: "Absolutely. We are an authorized retailer for all brands we carry. Every product comes with official warranty.",
    category: "Products",
  },
  {
    id: 4,
    question: "How can I track my order?",
    answer: "Once your order ships, you'll receive a tracking number via email. You can also track orders in your account dashboard.",
    category: "Orders",
  },
];

export const mockPartners: Partner[] = [
  { id: 1, name: "Apple", logo: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" },
  { id: 2, name: "Samsung", logo: "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg" },
  { id: 3, name: "Google", logo: "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" },
  { id: 4, name: "OnePlus", logo: "https://upload.wikimedia.org/wikipedia/commons/0/03/OnePlus_logo.svg" },
];

export const mockOffers: Offer[] = [
  {
    id: 1,
    title: "Flash Sale",
    description: "Up to 30% off flagship phones",
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
    discount: 30,
    end_date: "2025-07-15T23:59:59Z",
    link: "/products?sort=discount",
  },
  {
    id: 2,
    title: "Accessories Bundle",
    description: "Buy 2 get 1 free on all cases",
    image: "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600",
    discount: 33,
    end_date: "2025-07-20T23:59:59Z",
    link: "/products?category=accessories",
  },
];

export const mockAdvantages: Advantage[] = [
  { id: 1, title: "Free Shipping", description: "On orders over $50", icon: "Truck" },
  { id: 2, title: "2-Year Warranty", description: "Extended protection", icon: "Shield" },
  { id: 3, title: "24/7 Support", description: "Always here to help", icon: "Headphones" },
  { id: 4, title: "Secure Payment", description: "100% protected checkout", icon: "Lock" },
];

export const mockStats = [
  { label: "products", value: "2,500+", icon: "Package" },
  { label: "customers", value: "50K+", icon: "Users" },
  { label: "brands", value: "30+", icon: "Award" },
  { label: "orders", value: "100K+", icon: "ShoppingBag" },
];

export function getProductBySlug(slug: string): Product | undefined {
  return mockProducts.find((p) => p.slug === slug);
}

export function getBlogPostBySlug(slug: string): BlogPost | undefined {
  return mockBlogPosts.find((p) => p.slug === slug);
}
