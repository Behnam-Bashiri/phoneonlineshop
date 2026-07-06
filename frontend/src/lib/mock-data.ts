import type { Locale } from "@/lib/i18n";
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

const IMG = {
  iphone: "/images/products/iphone-16-pro-max.svg",
  samsung: "/images/products/samsung-galaxy-s25-ultra.svg",
  pixel: "/images/products/google-pixel-9-pro.svg",
  oneplus: "/images/products/oneplus-13.svg",
  xiaomi: "/images/products/xiaomi-15-ultra.svg",
  airpods: "/images/products/airpods-pro-3.svg",
} as const;

type Localized<T> = Record<Locale, T>;

const productsData: Localized<Product[]> = {
  en: [
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
      images: [{ id: 1, image: IMG.iphone, alt: "iPhone 16 Pro Max", is_primary: true }],
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
      images: [{ id: 2, image: IMG.samsung, alt: "Samsung Galaxy S25 Ultra", is_primary: true }],
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
      images: [{ id: 3, image: IMG.pixel, alt: "Google Pixel 9 Pro", is_primary: true }],
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
      images: [{ id: 4, image: IMG.oneplus, alt: "OnePlus 13", is_primary: true }],
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
      images: [{ id: 5, image: IMG.xiaomi, alt: "Xiaomi 15 Ultra", is_primary: true }],
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
      images: [{ id: 6, image: IMG.airpods, alt: "AirPods Pro 3", is_primary: true }],
      category: { id: 2, name: "Accessories", slug: "accessories" },
      brand: { id: 1, name: "Apple", slug: "apple" },
      tags: ["earbuds", "anc"],
      created_at: "2025-01-05T00:00:00Z",
    },
  ],
  fa: [
    {
      id: 1,
      name: "آیفون ۱۶ پرو مکس",
      slug: "iphone-16-pro-max",
      description:
        "پیشرفته‌ترین آیفون با تراشه A18 Pro، طراحی تیتانیومی و سیستم دوربین انقلابی.",
      short_description: "تیتانیوم. A18 Pro. کنترل دوربین.",
      price: 1199,
      compare_at_price: 1299,
      discount_percent: 8,
      sku: "IP16PM-256",
      stock: 45,
      is_featured: true,
      is_new: true,
      rating: 4.9,
      review_count: 128,
      images: [{ id: 1, image: IMG.iphone, alt: "آیفون ۱۶ پرو مکس", is_primary: true }],
      category: { id: 1, name: "گوشی هوشمند", slug: "smartphones" },
      brand: { id: 1, name: "اپل", slug: "apple" },
      specifications: {
        نمایشگر: "۶.۹ اینچ Super Retina XDR",
        تراشه: "A18 Pro",
        حافظه: "۲۵۶ گیگابایت",
        دوربین: "۴۸ مگاپیکسل اصلی + ۴۸ مگاپیکسل فوق‌عریض",
        باتری: "تا ۲۹ ساعت پخش ویدیو",
      },
      tags: ["پرچمدار", "5g", "تیتانیوم"],
      created_at: "2025-09-15T00:00:00Z",
    },
    {
      id: 2,
      name: "سامسونگ گلکسی S25 اولترا",
      slug: "samsung-galaxy-s25-ultra",
      description:
        "هوش مصنوعی گلکسی با طراحی پریمیوم، قلم S Pen، دوربین ۲۰۰ مگاپیکسل و Snapdragon 8 Elite.",
      short_description: "Galaxy AI. همراه با S Pen.",
      price: 1099,
      compare_at_price: 1199,
      discount_percent: 8,
      sku: "SGS25U-512",
      stock: 32,
      is_featured: true,
      is_new: true,
      rating: 4.8,
      review_count: 95,
      images: [{ id: 2, image: IMG.samsung, alt: "گلکسی S25 اولترا", is_primary: true }],
      category: { id: 1, name: "گوشی هوشمند", slug: "smartphones" },
      brand: { id: 2, name: "سامسونگ", slug: "samsung" },
      specifications: {
        نمایشگر: "۶.۸ اینچ Dynamic AMOLED 2X",
        تراشه: "Snapdragon 8 Elite",
        حافظه: "۵۱۲ گیگابایت",
        دوربین: "۲۰۰ مگاپیکسل",
        باتری: "۵۰۰۰ میلی‌آمپر",
      },
      tags: ["پرچمدار", "s-pen", "هوش-مصنوعی"],
      created_at: "2025-01-20T00:00:00Z",
    },
    {
      id: 3,
      name: "گوگل پیکسل ۹ پرو",
      slug: "google-pixel-9-pro",
      description: "بهترین هوش مصنوعی گوگل با طراحی خیره‌کننده و عکاسی محاسباتی بی‌نظیر.",
      short_description: "بهترین هوش مصنوعی گوگل.",
      price: 999,
      sku: "GP9P-256",
      stock: 28,
      is_featured: false,
      is_new: true,
      rating: 4.7,
      review_count: 67,
      images: [{ id: 3, image: IMG.pixel, alt: "پیکسل ۹ پرو", is_primary: true }],
      category: { id: 1, name: "گوشی هوشمند", slug: "smartphones" },
      brand: { id: 3, name: "گوگل", slug: "google" },
      tags: ["هوش-مصنوعی", "عکاسی"],
      created_at: "2025-02-01T00:00:00Z",
    },
    {
      id: 4,
      name: "وان‌پلاس ۱۳",
      slug: "oneplus-13",
      description: "هرگز تسلیم نشو — عملکرد پرچمدار با قیمت رقابتی.",
      short_description: "عملکرد پرچمدار با قیمت مناسب.",
      price: 799,
      compare_at_price: 899,
      discount_percent: 11,
      sku: "OP13-256",
      stock: 55,
      is_featured: true,
      is_new: false,
      rating: 4.6,
      review_count: 84,
      images: [{ id: 4, image: IMG.oneplus, alt: "وان‌پلاس ۱۳", is_primary: true }],
      category: { id: 1, name: "گوشی هوشمند", slug: "smartphones" },
      brand: { id: 4, name: "وان‌پلاس", slug: "oneplus" },
      tags: ["ارزش", "شارژ-سریع"],
      created_at: "2024-11-10T00:00:00Z",
    },
    {
      id: 5,
      name: "شیائومی ۱۵ اولترا",
      slug: "xiaomi-15-ultra",
      description: "اپتیک Leica و قدرت Snapdragon در یک قطبنه عکاسی.",
      short_description: "سیستم دوربین Leica.",
      price: 899,
      sku: "XM15U-512",
      stock: 40,
      is_featured: false,
      is_new: true,
      rating: 4.5,
      review_count: 52,
      images: [{ id: 5, image: IMG.xiaomi, alt: "شیائومی ۱۵ اولترا", is_primary: true }],
      category: { id: 1, name: "گوشی هوشمند", slug: "smartphones" },
      brand: { id: 5, name: "شیائومی", slug: "xiaomi" },
      tags: ["leica", "عکاسی"],
      created_at: "2025-03-01T00:00:00Z",
    },
    {
      id: 6,
      name: "ایرپادز پرو ۳",
      slug: "airpods-pro-3",
      description: "حذف نویز فعال بازتعریف‌شده با صدای تطبیقی و USB-C.",
      short_description: "ایرباد نسل جدید با ANC.",
      price: 249,
      sku: "APP3-WHT",
      stock: 120,
      is_featured: true,
      is_new: true,
      rating: 4.8,
      review_count: 210,
      images: [{ id: 6, image: IMG.airpods, alt: "ایرپادز پرو ۳", is_primary: true }],
      category: { id: 2, name: "لوازم جانبی", slug: "accessories" },
      brand: { id: 1, name: "اپل", slug: "apple" },
      tags: ["ایرباد", "anc"],
      created_at: "2025-01-05T00:00:00Z",
    },
  ],
};

const categoriesData: Localized<Category[]> = {
  en: [
    { id: 1, name: "Smartphones", slug: "smartphones", product_count: 156 },
    { id: 2, name: "Accessories", slug: "accessories", product_count: 342 },
    { id: 3, name: "Tablets", slug: "tablets", product_count: 48 },
    { id: 4, name: "Wearables", slug: "wearables", product_count: 89 },
    { id: 5, name: "Cases", slug: "cases", product_count: 520 },
    { id: 6, name: "Chargers", slug: "chargers", product_count: 178 },
  ],
  fa: [
    { id: 1, name: "گوشی هوشمند", slug: "smartphones", product_count: 156 },
    { id: 2, name: "لوازم جانبی", slug: "accessories", product_count: 342 },
    { id: 3, name: "تبلت", slug: "tablets", product_count: 48 },
    { id: 4, name: "پوشیدنی", slug: "wearables", product_count: 89 },
    { id: 5, name: "قاب", slug: "cases", product_count: 520 },
    { id: 6, name: "شارژر", slug: "chargers", product_count: 178 },
  ],
};

const brandsData: Localized<Brand[]> = {
  en: [
    { id: 1, name: "Apple", slug: "apple" },
    { id: 2, name: "Samsung", slug: "samsung" },
    { id: 3, name: "Google", slug: "google" },
    { id: 4, name: "OnePlus", slug: "oneplus" },
    { id: 5, name: "Xiaomi", slug: "xiaomi" },
    { id: 6, name: "Sony", slug: "sony" },
  ],
  fa: [
    { id: 1, name: "اپل", slug: "apple" },
    { id: 2, name: "سامسونگ", slug: "samsung" },
    { id: 3, name: "گوگل", slug: "google" },
    { id: 4, name: "وان‌پلاس", slug: "oneplus" },
    { id: 5, name: "شیائومی", slug: "xiaomi" },
    { id: 6, name: "سونی", slug: "sony" },
  ],
};

function buildHeroSlides(locale: Locale): HeroSlide[] {
  const products = productsData[locale];
  const cta = locale === "fa" ? "خرید کنید" : "Shop Now";
  const explore = locale === "fa" ? "مشاهده" : "Explore";
  const deals = locale === "fa" ? "مشاهده پیشنهادات" : "View Deals";

  return [
    {
      id: 1,
      title: products[0].name,
      subtitle:
        locale === "fa"
          ? "تیتانیوم. بسیار قوی. بسیار سبک. بسیار حرفه‌ای."
          : "Titanium. So strong. So light. So Pro.",
      image: IMG.iphone,
      link: "/products/iphone-16-pro-max",
      button_text: cta,
    },
    {
      id: 2,
      title: products[1].name,
      subtitle:
        locale === "fa"
          ? "Galaxy AI اینجاست. آینده را تجربه کنید."
          : "Galaxy AI is here. Experience the future.",
      image: IMG.samsung,
      link: "/products/samsung-galaxy-s25-ultra",
      button_text: explore,
    },
    {
      id: 3,
      title: locale === "fa" ? "حراج تابستانه" : "Summer Sale",
      subtitle:
        locale === "fa"
          ? "تا ۳۰٪ تخفیف روی دستگاه‌های منتخب"
          : "Up to 30% off on selected devices",
      image: IMG.oneplus,
      link: "/products?sort=discount",
      button_text: deals,
    },
  ];
}

function buildReviews(locale: Locale): Review[] {
  const products = productsData[locale];
  if (locale === "fa") {
    return [
      {
        id: 1,
        user: { name: "سارا م.", avatar: "" },
        product: products[0],
        rating: 5,
        title: "بهترین گوشی که داشتم",
        comment: "کیفیت دوربین فوق‌العاده است و بدنه تیتانیومی حس پریمیوم دارد.",
        created_at: "2025-06-01T00:00:00Z",
        is_verified: true,
      },
      {
        id: 2,
        user: { name: "علی ر.", avatar: "" },
        product: products[1],
        rating: 5,
        title: "Galaxy AI تحول‌آفرین است",
        comment: "قلم S Pen و قابلیت‌های هوش مصنوعی این گوشی را بی‌نظیر کرده.",
        created_at: "2025-05-28T00:00:00Z",
        is_verified: true,
      },
      {
        id: 3,
        user: { name: "جان د.", avatar: "" },
        product: products[2],
        rating: 4,
        title: "دوربین عالی، نرم‌افزار روان",
        comment: "عکس‌های پیکسل بی‌رقیب است. باتری می‌توانست بهتر باشد.",
        created_at: "2025-05-20T00:00:00Z",
        is_verified: true,
      },
    ];
  }
  return [
    {
      id: 1,
      user: { name: "Sarah M.", avatar: "" },
      product: products[0],
      rating: 5,
      title: "Best phone I've ever owned",
      comment: "The camera quality is incredible and the titanium build feels premium.",
      created_at: "2025-06-01T00:00:00Z",
      is_verified: true,
    },
    {
      id: 2,
      user: { name: "Ali R.", avatar: "" },
      product: products[1],
      rating: 5,
      title: "Galaxy AI is a game changer",
      comment: "The S Pen and AI features make this the most productive phone ever.",
      created_at: "2025-05-28T00:00:00Z",
      is_verified: true,
    },
    {
      id: 3,
      user: { name: "John D.", avatar: "" },
      product: products[2],
      rating: 4,
      title: "Great camera, smooth software",
      comment: "Pixel photos are unmatched. Battery could be better though.",
      created_at: "2025-05-20T00:00:00Z",
      is_verified: true,
    },
  ];
}

function buildBlogPosts(locale: Locale): BlogPost[] {
  if (locale === "fa") {
    return [
      {
        id: 1,
        title: "آیفون ۱۶ در برابر سامسونگ S25: کدام پرچمدار برنده است؟",
        slug: "iphone-16-vs-samsung-s25",
        excerpt: "دو بزرگ‌ترین پرچمدار ۲۰۲۵ را با هم مقایسه می‌کنیم.",
        content: "محتوای کامل مقاله...",
        image: IMG.oneplus,
        author: { name: "تیم فنی" },
        category: "بررسی",
        tags: ["مقایسه", "پرچمدار"],
        published_at: "2025-06-01T00:00:00Z",
        read_time: 8,
      },
      {
        id: 2,
        title: "بهترین گوشی‌های اقتصادی زیر ۵۰۰ دلار در ۲۰۲۵",
        slug: "best-budget-phones-2025",
        excerpt: "ویژگی‌های پریمیوم بدون قیمت پریمیوم.",
        content: "محتوای کامل مقاله...",
        image: IMG.pixel,
        author: { name: "راهنمای خرید" },
        category: "راهنما",
        tags: ["اقتصادی", "راهنما"],
        published_at: "2025-05-25T00:00:00Z",
        read_time: 6,
      },
      {
        id: 3,
        title: "چگونه قاب مناسب گوشی را انتخاب کنیم",
        slug: "choose-phone-case",
        excerpt: "محافظت در برابر استایل — انتخاب ایده‌آل خود را پیدا کنید.",
        content: "محتوای کامل مقاله...",
        image: IMG.airpods,
        author: { name: "لوازم جانبی" },
        category: "نکات",
        tags: ["لوازم-جانبی", "قاب"],
        published_at: "2025-05-15T00:00:00Z",
        read_time: 4,
      },
    ];
  }
  return [
    {
      id: 1,
      title: "iPhone 16 vs Samsung S25: Which Flagship Wins?",
      slug: "iphone-16-vs-samsung-s25",
      excerpt: "We compare the two biggest flagships of 2025 head to head.",
      content: "Full comparison article content...",
      image: IMG.oneplus,
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
      image: IMG.pixel,
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
      image: IMG.airpods,
      author: { name: "Accessories" },
      category: "Tips",
      tags: ["accessories", "cases"],
      published_at: "2025-05-15T00:00:00Z",
      read_time: 4,
    },
  ];
}

function buildFAQs(locale: Locale): FAQ[] {
  if (locale === "fa") {
    return [
      {
        id: 1,
        question: "سیاست بازگشت کالا چیست؟",
        answer:
          "ما ۳۰ روز ضمانت بازگشت بدون دردسر برای همه محصولات ارائه می‌دهیم. کالا باید در بسته‌بندی اصلی و سالم باشد.",
        category: "بازگشت",
      },
      {
        id: 2,
        question: "ارسال بین‌المللی دارید؟",
        answer: "بله، به بیش از ۵۰ کشور ارسال می‌کنیم. هزینه و زمان تحویل بسته به مقصد متفاوت است.",
        category: "ارسال",
      },
      {
        id: 3,
        question: "آیا همه محصولات اصل هستند؟",
        answer: "قطعاً. ما نمایندگی رسمی تمام برندها هستیم و هر محصول با گارانتی معتبر عرضه می‌شود.",
        category: "محصولات",
      },
      {
        id: 4,
        question: "چگونه سفارشم را پیگیری کنم؟",
        answer: "پس از ارسال، کد پیگیری از طریق ایمیل دریافت می‌کنید. همچنین در پنل کاربری قابل مشاهده است.",
        category: "سفارشات",
      },
    ];
  }
  return [
    {
      id: 1,
      question: "What is your return policy?",
      answer:
        "We offer a 30-day hassle-free return policy on all products. Items must be in original condition with all accessories included.",
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
}

function buildOffers(locale: Locale): Offer[] {
  if (locale === "fa") {
    return [
      {
        id: 1,
        title: "فروش ویژه",
        description: "تا ۳۰٪ تخفیف روی گوشی‌های پرچمدار",
        image: IMG.oneplus,
        discount: 30,
        end_date: "2025-07-15T23:59:59Z",
        link: "/products?sort=discount",
      },
      {
        id: 2,
        title: "بسته لوازم جانبی",
        description: "۲ عدد بخر، ۱ عدد هدیه بگیر روی همه قاب‌ها",
        image: IMG.airpods,
        discount: 33,
        end_date: "2025-07-20T23:59:59Z",
        link: "/products?category=accessories",
      },
    ];
  }
  return [
    {
      id: 1,
      title: "Flash Sale",
      description: "Up to 30% off flagship phones",
      image: IMG.oneplus,
      discount: 30,
      end_date: "2025-07-15T23:59:59Z",
      link: "/products?sort=discount",
    },
    {
      id: 2,
      title: "Accessories Bundle",
      description: "Buy 2 get 1 free on all cases",
      image: IMG.airpods,
      discount: 33,
      end_date: "2025-07-20T23:59:59Z",
      link: "/products?category=accessories",
    },
  ];
}

function buildAdvantages(locale: Locale): Advantage[] {
  if (locale === "fa") {
    return [
      { id: 1, title: "ارسال رایگان", description: "برای سفارش‌های بالای ۵۰ دلار", icon: "Truck" },
      { id: 2, title: "گارانتی ۲ ساله", description: "حفاظت تمدیدشده", icon: "Shield" },
      { id: 3, title: "پشتیبانی ۲۴/۷", description: "همیشه در کنار شما", icon: "Headphones" },
      { id: 4, title: "پرداخت امن", description: "۱۰۰٪ پرداخت محافظت‌شده", icon: "Lock" },
    ];
  }
  return [
    { id: 1, title: "Free Shipping", description: "On orders over $50", icon: "Truck" },
    { id: 2, title: "2-Year Warranty", description: "Extended protection", icon: "Shield" },
    { id: 3, title: "24/7 Support", description: "Always here to help", icon: "Headphones" },
    { id: 4, title: "Secure Payment", description: "100% protected checkout", icon: "Lock" },
  ];
}

const partnersData: Partner[] = [
  { id: 1, name: "Apple", logo: "" },
  { id: 2, name: "Samsung", logo: "" },
  { id: 3, name: "Google", logo: "" },
  { id: 4, name: "OnePlus", logo: "" },
];

const statsData = [
  { label: "products", value: "2,500+", icon: "Package" },
  { label: "customers", value: "50K+", icon: "Users" },
  { label: "brands", value: "30+", icon: "Award" },
  { label: "orders", value: "100K+", icon: "ShoppingBag" },
];

// Locale-aware getters
export function getMockProducts(locale: Locale): Product[] {
  return productsData[locale];
}

export function getMockCategories(locale: Locale): Category[] {
  return categoriesData[locale];
}

export function getMockBrands(locale: Locale): Brand[] {
  return brandsData[locale];
}

export function getMockHeroSlides(locale: Locale): HeroSlide[] {
  return buildHeroSlides(locale);
}

export function getMockReviews(locale: Locale): Review[] {
  return buildReviews(locale);
}

export function getMockBlogPosts(locale: Locale): BlogPost[] {
  return buildBlogPosts(locale);
}

export function getMockFAQs(locale: Locale): FAQ[] {
  return buildFAQs(locale);
}

export function getMockOffers(locale: Locale): Offer[] {
  return buildOffers(locale);
}

export function getMockAdvantages(locale: Locale): Advantage[] {
  return buildAdvantages(locale);
}

export function getMockPartners(locale: Locale): Partner[] {
  const brandMap = Object.fromEntries(
    brandsData[locale].map((b) => [b.slug, b.name])
  );
  const slugs = ["apple", "samsung", "google", "oneplus"];
  return partnersData.map((p, i) => ({
    ...p,
    name: brandMap[slugs[i]] ?? p.name,
  }));
}

export function getMockStats() {
  return statsData;
}

export function getProductBySlug(slug: string, locale: Locale = "en"): Product | undefined {
  return productsData[locale].find((p) => p.slug === slug);
}

export function getBlogPostBySlug(slug: string, locale: Locale = "en"): BlogPost | undefined {
  return buildBlogPosts(locale).find((p) => p.slug === slug);
}

// Backward-compatible default exports (English)
export const mockProducts = productsData.en;
export const mockCategories = categoriesData.en;
export const mockBrands = brandsData.en;
export const mockHeroSlides = buildHeroSlides("en");
export const mockReviews = buildReviews("en");
export const mockBlogPosts = buildBlogPosts("en");
export const mockFAQs = buildFAQs("en");
export const mockOffers = buildOffers("en");
export const mockAdvantages = buildAdvantages("en");
export const mockPartners = partnersData;
export const mockStats = statsData;
