"use client";

import Link from "next/link";
import Image from "next/image";
import { GitCompareArrows, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useCompareStore } from "@/stores/compare-store";
import { formatPrice } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function ComparePageContent({ locale }: { locale: Locale }) {
  const { items, removeItem, clearAll } = useCompareStore();
  const t = getTranslation(locale);

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <GitCompareArrows className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
        <h1 className="text-2xl font-bold">{t.compare.empty}</h1>
        <p className="text-muted-foreground mt-2">{t.compare.addProducts}</p>
        <Button variant="gradient" className="mt-6" asChild>
          <Link href={`/${locale}/products`}>{t.common.products}</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">{t.compare.title}</h1>
        <Button variant="outline" size="sm" onClick={clearAll}>{t.compare.clearAll}</Button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[600px]">
          <thead>
            <tr>
              <th className="p-4 text-left" />
              {items.map((product) => (
                <th key={product.id} className="p-4 text-center min-w-[200px]">
                  <div className="relative">
                    <Button variant="ghost" size="icon" className="absolute -top-2 -right-2 h-6 w-6" onClick={() => removeItem(product.id)}>
                      <X className="h-3 w-3" />
                    </Button>
                    <div className="relative w-32 h-32 mx-auto rounded-xl overflow-hidden bg-muted mb-3">
                      {product.images[0] && (
                        <Image src={product.images[0].image} alt={product.name} fill className="object-cover" />
                      )}
                    </div>
                    <Link href={`/${locale}/products/${product.slug}`} className="font-semibold text-sm hover:text-blue-600">
                      {product.name}
                    </Link>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr className="border-t">
              <td className="p-4 font-medium text-sm">Price</td>
              {items.map((p) => (
                <td key={p.id} className="p-4 text-center font-bold">{formatPrice(p.price, locale)}</td>
              ))}
            </tr>
            <tr className="border-t">
              <td className="p-4 font-medium text-sm">Brand</td>
              {items.map((p) => (
                <td key={p.id} className="p-4 text-center text-sm">{p.brand?.name || "-"}</td>
              ))}
            </tr>
            <tr className="border-t">
              <td className="p-4 font-medium text-sm">Rating</td>
              {items.map((p) => (
                <td key={p.id} className="p-4 text-center text-sm">{p.rating} ({p.review_count})</td>
              ))}
            </tr>
            <tr className="border-t">
              <td className="p-4 font-medium text-sm">Stock</td>
              {items.map((p) => (
                <td key={p.id} className="p-4 text-center text-sm">{p.stock > 0 ? "In Stock" : "Out of Stock"}</td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
