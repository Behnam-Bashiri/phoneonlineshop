import type { Metadata } from "next";
import { Suspense } from "react";
import { ProductsCatalog } from "@/components/product/products-catalog";
import { ProductGridSkeleton } from "@/components/product/product-skeleton";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);
  return { title: t.products.title };
}

export default async function ProductsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <Suspense fallback={<ProductGridSkeleton />}>
      <ProductsCatalog locale={locale as Locale} />
    </Suspense>
  );
}
