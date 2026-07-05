"use client";

import Link from "next/link";
import { Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductCard } from "@/components/product/product-card";
import { useWishlistStore } from "@/stores/wishlist-store";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function WishlistPageContent({ locale }: { locale: Locale }) {
  const items = useWishlistStore((s) => s.items);
  const t = getTranslation(locale);

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <Heart className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
        <h1 className="text-2xl font-bold">{t.wishlist.empty}</h1>
        <p className="text-muted-foreground mt-2">{t.wishlist.emptyDesc}</p>
        <Button variant="gradient" className="mt-6" asChild>
          <Link href={`/${locale}/products`}>{t.cart.continueShopping}</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <h1 className="text-3xl font-bold mb-8">{t.wishlist.title}</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        {items.map((product) => (
          <ProductCard key={product.id} product={product} locale={locale} />
        ))}
      </div>
    </div>
  );
}
