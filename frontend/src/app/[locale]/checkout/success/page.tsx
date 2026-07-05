import Link from "next/link";
import { CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);
  return { title: t.checkout.success.title };
}

export default async function CheckoutSuccessPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ order?: string }>;
}) {
  const { locale } = await params;
  const { order } = await searchParams;
  const t = getTranslation(locale as Locale);

  return (
    <div className="container mx-auto px-4 py-16 text-center max-w-lg">
      <div className="glass-card p-8 md:p-12">
        <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
        <h1 className="text-2xl md:text-3xl font-bold">{t.checkout.success.title}</h1>
        <p className="text-muted-foreground mt-2">{t.checkout.success.subtitle}</p>
        {order && (
          <p className="mt-4 font-mono text-sm bg-muted rounded-lg px-4 py-2 inline-block">
            {t.checkout.success.orderNumber}: {order}
          </p>
        )}
        <div className="flex flex-col sm:flex-row gap-3 mt-8 justify-center">
          <Button variant="gradient" asChild>
            <Link href={`/${locale}/account/orders`}>
              {t.checkout.success.trackOrder}
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href={`/${locale}/products`}>
              {t.checkout.success.continueShopping}
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
