import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ProductDetail } from "@/components/product/product-detail";
import { getProductBySlug, getMockProducts } from "@/lib/mock-data";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { locale, slug } = await params;
  const loc = locale as Locale;
  const product = getProductBySlug(slug, loc);
  const t = getTranslation(loc);
  if (!product) return { title: t.products.noProducts };
  return {
    title: product.name,
    description: product.short_description || product.description,
  };
}

export function generateStaticParams() {
  return getMockProducts("en").map((p) => ({ slug: p.slug }));
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  const loc = locale as Locale;
  const product = getProductBySlug(slug, loc);

  if (!product) notFound();

  const mockProducts = getMockProducts(loc);
  const relatedProducts = mockProducts
    .filter((p) => p.id !== product.id && p.category.slug === product.category.slug)
    .slice(0, 4);

  return (
    <ProductDetail
      product={product}
      relatedProducts={relatedProducts}
      locale={loc}
    />
  );
}
