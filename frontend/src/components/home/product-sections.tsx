"use client";

import Link from "next/link";
import { SectionHeader } from "@/components/common/section-header";
import { ViewAllLink } from "@/components/common/view-all-link";
import { ProductCard } from "@/components/product/product-card";
import { FadeIn } from "@/components/common/motion-wrapper";
import { getLucideIcon } from "@/lib/icons";
import { getTranslation, translate } from "@/lib/translations";
import type { Product } from "@/types";
import type { Locale } from "@/lib/i18n";

interface ProductSectionProps {
  title: string;
  products: Product[];
  locale: Locale;
  viewAllHref?: string;
}

export function ProductSection({
  title,
  products,
  locale,
  viewAllHref,
}: ProductSectionProps) {
  const t = getTranslation(locale);

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <div className="flex items-end justify-between mb-8">
          <SectionHeader title={title} className="mb-0" />
          {viewAllHref && (
            <ViewAllLink href={viewAllHref} label={t.common.viewAll} locale={locale} />
          )}
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {products.map((product, i) => (
            <FadeIn key={product.id} delay={i * 0.05}>
              <ProductCard product={product} locale={locale} />
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

interface BrandGridProps {
  brands: { id: number; name: string; slug: string; logo?: string }[];
  locale: Locale;
  title: string;
}

export function BrandGrid({ brands, locale, title }: BrandGridProps) {
  return (
    <section className="py-12 md:py-16 gradient-bg">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <div className="grid grid-cols-3 md:grid-cols-6 gap-4 md:gap-6">
          {brands.map((brand, i) => (
            <FadeIn key={brand.id} delay={i * 0.05}>
              <Link
                href={`/${locale}/products?brand=${brand.slug}`}
                className="glass-card flex items-center justify-center h-20 md:h-24 p-4 hover:shadow-lg transition-shadow"
              >
                <span className="font-semibold text-sm md:text-base text-center">
                  {brand.name}
                </span>
              </Link>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

interface CategoryGridProps {
  categories: { id: number; name: string; slug: string; product_count?: number }[];
  locale: Locale;
  title: string;
}

export function CategoryGrid({ categories, locale, title }: CategoryGridProps) {
  const icons = ["Smartphone", "Headphones", "Tablet", "Watch", "Shield", "Zap"];

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories.map((cat, i) => {
            const IconComponent = getLucideIcon(icons[i % icons.length]);
            return (
              <FadeIn key={cat.id} delay={i * 0.05}>
                <Link
                  href={`/${locale}/products?category=${cat.slug}`}
                  className="glass-card group flex flex-col items-center p-6 hover:shadow-lg transition-all hover:-translate-y-1"
                >
                  <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                    <IconComponent className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <span className="font-medium text-sm text-center">{cat.name}</span>
                  {cat.product_count && (
                    <span className="text-xs text-muted-foreground mt-1">
                      {translate(locale, "common.items", { count: cat.product_count })}
                    </span>
                  )}
                </Link>
              </FadeIn>
            );
          })}
        </div>
      </div>
    </section>
  );
}
