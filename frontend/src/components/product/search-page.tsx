"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Search } from "lucide-react";
import { ProductCard } from "@/components/product/product-card";
import { ProductGridSkeleton } from "@/components/product/product-skeleton";
import { getMockProducts } from "@/lib/mock-data";
import { getTranslation, translate } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

function SearchResults({ locale }: { locale: Locale }) {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const t = getTranslation(locale);
  const mockProducts = getMockProducts(locale);

  const results = query
    ? mockProducts.filter(
        (p) =>
          p.name.toLowerCase().includes(query.toLowerCase()) ||
          p.description.toLowerCase().includes(query.toLowerCase()) ||
          p.brand?.name.toLowerCase().includes(query.toLowerCase())
      )
    : [];

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <h1 className="text-3xl font-bold mb-2">{t.search.title}</h1>
      {query && (
        <p className="text-muted-foreground mb-8">
          {translate(locale, "search.for", { query })}
        </p>
      )}
      {!query ? (
        <div className="text-center py-16">
          <Search className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">{t.common.searchPlaceholder}</p>
        </div>
      ) : results.length === 0 ? (
        <p className="text-center text-muted-foreground py-16">{t.search.noResults}</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {results.map((product) => (
            <ProductCard key={product.id} product={product} locale={locale} />
          ))}
        </div>
      )}
    </div>
  );
}

export function SearchPageContent({ locale }: { locale: Locale }) {
  return (
    <Suspense fallback={<ProductGridSkeleton />}>
      <SearchResults locale={locale} />
    </Suspense>
  );
}
