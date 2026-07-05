"use client";

import Image from "next/image";
import Link from "next/link";
import { Minus, Plus, Trash2, ShoppingBag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { useCartStore } from "@/stores/cart-store";
import { formatPrice } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

interface CartPageContentProps {
  locale: Locale;
}

export function CartPageContent({ locale }: CartPageContentProps) {
  const { items, updateQuantity, removeItem, getSubtotal, couponCode, setCoupon } =
    useCartStore();
  const t = getTranslation(locale);
  const subtotal = getSubtotal();
  const shipping = subtotal > 50 ? 0 : 9.99;
  const total = subtotal + shipping;

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <ShoppingBag className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
        <h1 className="text-2xl font-bold">{t.cart.empty}</h1>
        <p className="text-muted-foreground mt-2">{t.cart.emptyDesc}</p>
        <Button variant="gradient" className="mt-6" asChild>
          <Link href={`/${locale}/products`}>{t.cart.continueShopping}</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <h1 className="text-3xl font-bold mb-8">{t.cart.title}</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => {
            const price = item.variant?.price ?? item.product.price;
            const image = item.product.images[0]?.image;
            return (
              <div key={`${item.product.id}-${item.variant?.id}`} className="glass-card p-4 flex gap-4">
                <div className="relative w-24 h-24 rounded-xl overflow-hidden bg-muted shrink-0">
                  {image && <Image src={image} alt={item.product.name} fill className="object-cover" />}
                </div>
                <div className="flex-1">
                  <Link
                    href={`/${locale}/products/${item.product.slug}`}
                    className="font-semibold hover:text-blue-600 transition-colors"
                  >
                    {item.product.name}
                  </Link>
                  <p className="text-sm text-muted-foreground mt-1">
                    {formatPrice(price, locale)}
                  </p>
                  <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center border rounded-lg">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() =>
                          updateQuantity(item.product.id, item.quantity - 1, item.variant?.id)
                        }
                      >
                        <Minus className="h-3 w-3" />
                      </Button>
                      <span className="w-8 text-center text-sm">{item.quantity}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() =>
                          updateQuantity(item.product.id, item.quantity + 1, item.variant?.id)
                        }
                      >
                        <Plus className="h-3 w-3" />
                      </Button>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="font-semibold">
                        {formatPrice(price * item.quantity, locale)}
                      </span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-destructive h-8 w-8"
                        onClick={() => removeItem(item.product.id, item.variant?.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div>
          <div className="glass-card p-6 sticky top-24">
            <h2 className="font-semibold text-lg mb-4">{t.checkout.orderSummary}</h2>
            <div className="flex gap-2 mb-4">
              <Input
                placeholder={t.cart.coupon}
                value={couponCode || ""}
                onChange={(e) => setCoupon(e.target.value || null)}
              />
              <Button variant="outline">{t.cart.applyCoupon}</Button>
            </div>
            <Separator className="my-4" />
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">{t.cart.subtotal}</span>
                <span>{formatPrice(subtotal, locale)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">{t.cart.shipping}</span>
                <span>{shipping === 0 ? "Free" : formatPrice(shipping, locale)}</span>
              </div>
            </div>
            <Separator className="my-4" />
            <div className="flex justify-between font-bold text-lg">
              <span>{t.cart.total}</span>
              <span>{formatPrice(total, locale)}</span>
            </div>
            <Button variant="gradient" className="w-full mt-6" size="lg" asChild>
              <Link href={`/${locale}/checkout`}>{t.cart.proceedToCheckout}</Link>
            </Button>
            <Button variant="ghost" className="w-full mt-2" asChild>
              <Link href={`/${locale}/products`}>{t.cart.continueShopping}</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
