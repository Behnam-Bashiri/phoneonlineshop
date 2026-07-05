"use client";

import Image from "next/image";
import Link from "next/link";
import { Heart, ShoppingCart, Star, GitCompareArrows } from "lucide-react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn, formatPrice } from "@/lib/utils";
import { useCartStore } from "@/stores/cart-store";
import { useWishlistStore } from "@/stores/wishlist-store";
import { useCompareStore } from "@/stores/compare-store";
import { toast } from "@/hooks/use-toast";
import type { Product } from "@/types";
import type { Locale } from "@/lib/i18n";

interface ProductCardProps {
  product: Product;
  locale: Locale;
  view?: "grid" | "list";
}

export function ProductCard({ product, locale, view = "grid" }: ProductCardProps) {
  const addToCart = useCartStore((s) => s.addItem);
  const { toggleItem, isInWishlist } = useWishlistStore();
  const { addItem: addToCompare, isInCompare } = useCompareStore();
  const inWishlist = isInWishlist(product.id);
  const inCompare = isInCompare(product.id);
  const primaryImage = product.images[0]?.image;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addToCart(product);
    toast({ title: "Added to cart", description: product.name, variant: "success" });
  };

  if (view === "list") {
    return (
      <Link href={`/${locale}/products/${product.slug}`}>
        <Card className="group overflow-hidden glass-card hover:shadow-xl transition-all duration-300">
          <div className="flex flex-col sm:flex-row gap-4 p-4">
            <div className="relative w-full sm:w-48 h-48 shrink-0 rounded-xl overflow-hidden bg-muted">
              {primaryImage && (
                <Image
                  src={primaryImage}
                  alt={product.name}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500"
                />
              )}
              {product.discount_percent && (
                <Badge className="absolute top-2 left-2" variant="destructive">
                  -{product.discount_percent}%
                </Badge>
              )}
            </div>
            <div className="flex-1 flex flex-col justify-between">
              <div>
                <p className="text-xs text-muted-foreground">{product.brand?.name}</p>
                <h3 className="font-semibold text-lg mt-1">{product.name}</h3>
                <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                  {product.short_description}
                </p>
                <div className="flex items-center gap-1 mt-2">
                  <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                  <span className="text-sm font-medium">{product.rating}</span>
                  <span className="text-xs text-muted-foreground">
                    ({product.review_count})
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between mt-4">
                <div className="flex items-baseline gap-2">
                  <span className="text-xl font-bold">
                    {formatPrice(product.price, locale)}
                  </span>
                  {product.compare_at_price && (
                    <span className="text-sm text-muted-foreground line-through">
                      {formatPrice(product.compare_at_price, locale)}
                    </span>
                  )}
                </div>
                <Button size="sm" variant="gradient" onClick={handleAddToCart}>
                  <ShoppingCart className="h-4 w-4 mr-1" />
                  Add to Cart
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </Link>
    );
  }

  return (
    <Link href={`/${locale}/products/${product.slug}`}>
      <motion.div whileHover={{ y: -4 }} transition={{ duration: 0.2 }}>
        <Card className="group overflow-hidden glass-card hover:shadow-xl transition-shadow duration-300 h-full">
          <div className="relative aspect-square overflow-hidden bg-muted">
            {primaryImage && (
              <Image
                src={primaryImage}
                alt={product.name}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
            )}
            <div className="absolute top-2 left-2 flex flex-col gap-1">
              {product.is_new && <Badge variant="success">New</Badge>}
              {product.discount_percent && (
                <Badge variant="destructive">-{product.discount_percent}%</Badge>
              )}
            </div>
            <div className="absolute top-2 right-2 flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <Button
                size="icon"
                variant="glass"
                className="h-8 w-8 rounded-full"
                onClick={(e) => {
                  e.preventDefault();
                  toggleItem(product);
                }}
              >
                <Heart
                  className={cn(
                    "h-4 w-4",
                    inWishlist && "fill-red-500 text-red-500"
                  )}
                />
              </Button>
              <Button
                size="icon"
                variant="glass"
                className="h-8 w-8 rounded-full"
                onClick={(e) => {
                  e.preventDefault();
                  addToCompare(product);
                }}
              >
                <GitCompareArrows
                  className={cn("h-4 w-4", inCompare && "text-blue-500")}
                />
              </Button>
            </div>
          </div>
          <CardContent className="p-4">
            <p className="text-xs text-muted-foreground">{product.brand?.name}</p>
            <h3 className="font-semibold mt-1 line-clamp-1">{product.name}</h3>
            <div className="flex items-center gap-1 mt-1">
              <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
              <span className="text-xs font-medium">{product.rating}</span>
              <span className="text-xs text-muted-foreground">
                ({product.review_count})
              </span>
            </div>
            <div className="flex items-center justify-between mt-3">
              <div className="flex items-baseline gap-1.5">
                <span className="font-bold">
                  {formatPrice(product.price, locale)}
                </span>
                {product.compare_at_price && (
                  <span className="text-xs text-muted-foreground line-through">
                    {formatPrice(product.compare_at_price, locale)}
                  </span>
                )}
              </div>
              <Button
                size="icon"
                variant="gradient"
                className="h-8 w-8 rounded-full"
                onClick={handleAddToCart}
              >
                <ShoppingCart className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </Link>
  );
}
