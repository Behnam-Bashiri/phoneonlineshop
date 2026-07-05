import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ProductDetail } from "@/components/product/product-detail";
import { getProductBySlug, mockProducts } from "@/lib/mock-data";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) return { title: "Product Not Found" };
  return {
    title: product.name,
    description: product.short_description || product.description,
  };
}

export function generateStaticParams() {
  return mockProducts.map((p) => ({ slug: p.slug }));
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  const product = getProductBySlug(slug);

  if (!product) notFound();

  const relatedProducts = mockProducts
    .filter((p) => p.id !== product.id && p.category.slug === product.category.slug)
    .slice(0, 4);

  return (
    <ProductDetail
      product={product}
      relatedProducts={relatedProducts}
      locale={locale as Locale}
    />
  );
}
