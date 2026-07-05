import type { Metadata } from "next";
import { HeroSlider } from "@/components/home/hero-slider";
import {
  ProductSection,
  BrandGrid,
  CategoryGrid,
} from "@/components/home/product-sections";
import { OffersSection, CountdownBanner } from "@/components/home/offers-section";
import { ReviewsSection } from "@/components/home/reviews-section";
import { BlogSection } from "@/components/home/blog-section";
import { NewsletterSection } from "@/components/home/newsletter-section";
import { FAQSection } from "@/components/home/faq-section";
import { StatsSection } from "@/components/home/stats-section";
import { AdvantagesSection } from "@/components/home/advantages-section";
import { AppBanner } from "@/components/home/app-banner";
import { InstagramSection } from "@/components/home/instagram-section";
import { PartnersSection } from "@/components/home/partners-section";
import {
  mockProducts,
  mockHeroSlides,
  mockBrands,
  mockCategories,
  mockOffers,
  mockReviews,
  mockBlogPosts,
  mockFAQs,
  mockStats,
  mockAdvantages,
  mockPartners,
} from "@/lib/mock-data";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);
  return {
    title: "PhonyShop - Premium Phones & Accessories",
    description: t.home.hero.subtitle,
  };
}

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);
  const loc = locale as Locale;

  const featured = mockProducts.filter((p) => p.is_featured);
  const latest = [...mockProducts].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
  const popular = [...mockProducts].sort((a, b) => b.review_count - a.review_count);

  return (
    <>
      <div className="container mx-auto px-4 pt-4 md:pt-8">
        <HeroSlider slides={mockHeroSlides} locale={loc} />
      </div>

      <AdvantagesSection advantages={mockAdvantages} title={t.home.advantages} />

      <ProductSection
        title={t.home.featured}
        products={featured}
        locale={loc}
        viewAllHref={`/${locale}/products?featured=true`}
      />

      <CountdownBanner
        endDate="2025-07-15T23:59:59Z"
        title="Summer Mega Sale"
        locale={loc}
      />

      <OffersSection offers={mockOffers} locale={loc} title={t.home.offers} />

      <CategoryGrid
        categories={mockCategories}
        locale={loc}
        title={t.home.categories}
      />

      <ProductSection
        title={t.home.latest}
        products={latest.slice(0, 4)}
        locale={loc}
        viewAllHref={`/${locale}/products?sort=newest`}
      />

      <BrandGrid brands={mockBrands} locale={loc} title={t.home.brands} />

      <ProductSection
        title={t.home.popular}
        products={popular.slice(0, 4)}
        locale={loc}
        viewAllHref={`/${locale}/products?sort=popular`}
      />

      <StatsSection stats={mockStats} locale={loc} />

      <ReviewsSection reviews={mockReviews} locale={loc} title={t.home.reviews} />

      <BlogSection posts={mockBlogPosts} locale={loc} title={t.home.blog} />

      <InstagramSection title={t.home.instagram} />

      <PartnersSection partners={mockPartners} title={t.home.partners} />

      <FAQSection faqs={mockFAQs} title={t.home.faq} />

      <NewsletterSection locale={loc} />

      <AppBanner locale={loc} />
    </>
  );
}
