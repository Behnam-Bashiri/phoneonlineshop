"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Check, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useCartStore } from "@/stores/cart-store";
import { formatPrice, cn } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

interface CheckoutContentProps {
  locale: Locale;
}

export function CheckoutContent({ locale }: CheckoutContentProps) {
  const [step, setStep] = useState(0);
  const [paymentMethod, setPaymentMethod] = useState("online");
  const router = useRouter();
  const { items, getSubtotal, clearCart } = useCartStore();
  const t = getTranslation(locale);
  const subtotal = getSubtotal();
  const shipping = subtotal > 50 ? 0 : 9.99;
  const total = subtotal + shipping;

  const steps = [
    t.checkout.steps.shipping,
    t.checkout.steps.payment,
    t.checkout.steps.review,
  ];

  const handlePlaceOrder = async () => {
    await new Promise((r) => setTimeout(r, 1500));
    clearCart();
    router.push(`/${locale}/checkout/success?order=PS-${Date.now()}`);
  };

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-muted-foreground">Your cart is empty.</p>
        <Button variant="gradient" className="mt-4" asChild>
          <Link href={`/${locale}/products`}>{t.cart.continueShopping}</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 md:py-12 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">{t.checkout.title}</h1>

      <div className="flex items-center justify-center mb-12">
        {steps.map((s, i) => (
          <div key={s} className="flex items-center">
            <div
              className={cn(
                "h-10 w-10 rounded-full flex items-center justify-center text-sm font-medium transition-colors",
                i <= step
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-muted-foreground"
              )}
            >
              {i < step ? <Check className="h-5 w-5" /> : i + 1}
            </div>
            <span className="ml-2 text-sm font-medium hidden sm:inline">{s}</span>
            {i < steps.length - 1 && (
              <ChevronRight className="h-4 w-4 mx-4 text-muted-foreground" />
            )}
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          {step === 0 && (
            <div className="glass-card p-6 space-y-4">
              <h2 className="font-semibold text-lg">{t.checkout.shippingAddress}</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>First Name</Label>
                  <Input placeholder="John" />
                </div>
                <div className="space-y-2">
                  <Label>Last Name</Label>
                  <Input placeholder="Doe" />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Address</Label>
                <Input placeholder="123 Main St" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>City</Label>
                  <Input placeholder="San Francisco" />
                </div>
                <div className="space-y-2">
                  <Label>Postal Code</Label>
                  <Input placeholder="94102" />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Phone</Label>
                <Input placeholder="+1 555 123 4567" />
              </div>
              <Button variant="gradient" onClick={() => setStep(1)} className="mt-4">
                {t.common.next}
              </Button>
            </div>
          )}

          {step === 1 && (
            <div className="glass-card p-6 space-y-4">
              <h2 className="font-semibold text-lg">{t.checkout.paymentMethod}</h2>
              <div className="space-y-3">
                {[
                  { value: "online", label: "Credit / Debit Card" },
                  { value: "wallet", label: "Wallet Balance" },
                  { value: "cod", label: "Cash on Delivery" },
                ].map((method) => (
                  <label
                    key={method.value}
                    className={cn(
                      "flex items-center gap-3 p-4 rounded-xl border cursor-pointer transition-colors",
                      paymentMethod === method.value
                        ? "border-primary bg-primary/5"
                        : "hover:bg-accent"
                    )}
                  >
                    <input
                      type="radio"
                      name="payment"
                      value={method.value}
                      checked={paymentMethod === method.value}
                      onChange={() => setPaymentMethod(method.value)}
                      className="accent-primary"
                    />
                    {method.label}
                  </label>
                ))}
              </div>
              <div className="flex gap-3 mt-4">
                <Button variant="outline" onClick={() => setStep(0)}>
                  {t.common.back}
                </Button>
                <Button variant="gradient" onClick={() => setStep(2)}>
                  {t.common.next}
                </Button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="glass-card p-6 space-y-4">
              <h2 className="font-semibold text-lg">{t.checkout.steps.review}</h2>
              {items.map((item) => (
                <div
                  key={`${item.product.id}-${item.variant?.id}`}
                  className="flex justify-between text-sm"
                >
                  <span>
                    {item.product.name} x{item.quantity}
                  </span>
                  <span>
                    {formatPrice(
                      (item.variant?.price ?? item.product.price) * item.quantity,
                      locale
                    )}
                  </span>
                </div>
              ))}
              <Separator />
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => setStep(1)}>
                  {t.common.back}
                </Button>
                <Button variant="gradient" onClick={handlePlaceOrder}>
                  {t.checkout.placeOrder}
                </Button>
              </div>
            </div>
          )}
        </div>

        <div>
          <div className="glass-card p-6 sticky top-24">
            <h3 className="font-semibold mb-4">{t.checkout.orderSummary}</h3>
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
            <div className="flex justify-between font-bold">
              <span>{t.cart.total}</span>
              <span>{formatPrice(total, locale)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
