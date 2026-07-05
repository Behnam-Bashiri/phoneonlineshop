"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Star,
  Heart,
  ShoppingCart,
  GitCompareArrows,
  Share2,
  Minus,
  Plus,
  Truck,
  Shield,
  RotateCcw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { ProductCard } from "@/components/product/product-card";
import { FadeIn } from "@/components/common/motion-wrapper";
import { useCartStore } from "@/stores/cart-store";
import { useWishlistStore } from "@/stores/wishlist-store";
import { useCompareStore } from "@/stores/compare-store";
import { toast } from "@/hooks/use-toast";
import { cn, formatPrice } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Product } from "@/types";
import type { Locale } from "@/lib/i18n";

interface ProductDetailProps {
  product: Product;
  relatedProducts: Product[];
  locale: Locale;
}

export function ProductDetail({
  product,
  relatedProducts,
  locale,
}: ProductDetailProps) {
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const addToCart = useCartStore((s) => s.addItem);
  const { toggleItem, isInWishlist } = useWishlistStore();
  const { addItem: addToCompare, isInCompare } = useCompareStore();
  const t = getTranslation(locale);
  const inWishlist = isInWishlist(product.id);

  const handleAddToCart = () => {
    addToCart(product, undefined, quantity);
    toast({ title: "Added to cart", description: product.name, variant: "success" });
  };

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
        <FadeIn direction="left">
          <div className="space-y-4">
            <div className="relative aspect-square rounded-3xl overflow-hidden bg-muted glass-card">
              {product.images[selectedImage] && (
                <Image
                  src={product.images[selectedImage].image}
                  alt={product.name}
                  fill
                  className="object-cover"
                  priority
                />
              )}
              {product.discount_percent && (
                <Badge variant="destructive" className="absolute top-4 left-4">
                  -{product.discount_percent}%
                </Badge>
              )}
            </div>
            {product.images.length > 1 && (
              <div className="flex gap-3">
                {product.images.map((img, i) => (
                  <button
                    key={img.id}
                    onClick={() => setSelectedImage(i)}
                    className={cn(
                      "relative w-20 h-20 rounded-xl overflow-hidden border-2 transition-colors",
                      selectedImage === i ? "border-primary" : "border-transparent"
                    )}
                  >
                    <Image src={img.image} alt="" fill className="object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>
        </FadeIn>

        <FadeIn direction="right">
          <div>
            <p className="text-sm text-muted-foreground">{product.brand?.name}</p>
            <h1 className="text-3xl md:text-4xl font-bold mt-1">{product.name}</h1>

            <div className="flex items-center gap-3 mt-3">
              <div className="flex items-center gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={cn(
                      "h-4 w-4",
                      i < Math.floor(product.rating)
                        ? "fill-amber-400 text-amber-400"
                        : "text-muted"
                    )}
                  />
                ))}
              </div>
              <span className="text-sm font-medium">{product.rating}</span>
              <span className="text-sm text-muted-foreground">
                ({product.review_count} reviews)
              </span>
            </div>

            <div className="flex items-baseline gap-3 mt-6">
              <span className="text-3xl font-bold">
                {formatPrice(product.price, locale)}
              </span>
              {product.compare_at_price && (
                <span className="text-lg text-muted-foreground line-through">
                  {formatPrice(product.compare_at_price, locale)}
                </span>
              )}
            </div>

            <p className="text-muted-foreground mt-4 leading-relaxed">
              {product.short_description || product.description}
            </p>

            <div className="flex items-center gap-4 mt-4 text-sm">
              <span className="text-muted-foreground">{t.product.sku}: {product.sku}</span>
              <Badge variant={product.stock > 0 ? "success" : "destructive"}>
                {product.stock > 0 ? t.common.inStock : t.common.outOfStock}
              </Badge>
            </div>

            <Separator className="my-6" />

            <div className="flex items-center gap-4">
              <div className="flex items-center border rounded-xl">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                >
                  <Minus className="h-4 w-4" />
                </Button>
                <span className="w-12 text-center font-medium">{quantity}</span>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 mt-6">
              <Button variant="gradient" size="lg" className="flex-1" onClick={handleAddToCart}>
                <ShoppingCart className="mr-2 h-5 w-5" />
                {t.common.addToCart}
              </Button>
              <Button variant="outline" size="lg" className="flex-1" asChild>
                <Link href={`/${locale}/checkout`}>{t.common.buyNow}</Link>
              </Button>
            </div>

            <div className="flex gap-2 mt-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => toggleItem(product)}
              >
                <Heart className={cn("h-4 w-4 mr-1", inWishlist && "fill-red-500 text-red-500")} />
                {inWishlist ? t.product.removeFromWishlist : t.product.addToWishlist}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => addToCompare(product)}
              >
                <GitCompareArrows className="h-4 w-4 mr-1" />
                {t.product.addToCompare}
              </Button>
              <Button variant="ghost" size="sm">
                <Share2 className="h-4 w-4 mr-1" />
                {t.product.share}
              </Button>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-8">
              {[
                { icon: Truck, text: "Free Shipping" },
                { icon: Shield, text: "2-Year Warranty" },
                { icon: RotateCcw, text: "30-Day Returns" },
              ].map(({ icon: Icon, text }) => (
                <div key={text} className="text-center glass-card p-3">
                  <Icon className="h-5 w-5 mx-auto text-blue-600" />
                  <p className="text-xs mt-1 font-medium">{text}</p>
                </div>
              ))}
            </div>
          </div>
        </FadeIn>
      </div>

      <div className="mt-16">
        <Tabs defaultValue="description">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="description">{t.product.description}</TabsTrigger>
            <TabsTrigger value="specs">{t.product.specifications}</TabsTrigger>
            <TabsTrigger value="reviews">{t.product.reviews}</TabsTrigger>
          </TabsList>
          <TabsContent value="description" className="mt-6">
            <div className="glass-card p-6 prose dark:prose-invert max-w-none">
              <p>{product.description}</p>
            </div>
          </TabsContent>
          <TabsContent value="specs" className="mt-6">
            <div className="glass-card p-6">
              {product.specifications ? (
                <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key} className="flex justify-between border-b pb-2">
                      <dt className="text-muted-foreground">{key}</dt>
                      <dd className="font-medium">{value}</dd>
                    </div>
                  ))}
                </dl>
              ) : (
                <p className="text-muted-foreground">No specifications available.</p>
              )}
            </div>
          </TabsContent>
          <TabsContent value="reviews" className="mt-6">
            <div className="glass-card p-6 text-center text-muted-foreground">
              Reviews will be loaded from the API.
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {relatedProducts.length > 0 && (
        <section className="mt-16">
          <h2 className="text-2xl font-bold mb-6">{t.product.related}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
            {relatedProducts.map((p) => (
              <ProductCard key={p.id} product={p} locale={locale} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
