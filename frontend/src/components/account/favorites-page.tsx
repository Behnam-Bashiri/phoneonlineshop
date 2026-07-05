"use client";

import Link from "next/link";
import { Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductCard } from "@/components/product/product-card";
import { useWishlistStore } from "@/stores/wishlist-store";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function FavoritesPage({ locale }: { locale: Locale }) {
  const items = useWishlistStore((s) => s.items);
  const t = getTranslation(locale);

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <Heart className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
        <h1 className="text-2xl font-bold">{t.wishlist.empty}</h1>
        <Button variant="gradient" className="mt-4" asChild>
          <Link href={`/${locale}/products`}>{t.cart.continueShopping}</Link>
        </Button>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.favorites}</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {items.map((product) => (
          <ProductCard key={product.id} product={product} locale={locale} />
        ))}
      </div>
    </div>
  );
}
