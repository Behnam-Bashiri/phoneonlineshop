import Link from "next/link";
import { XCircle } from "lucide-react";
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
  return { title: t.checkout.failed.title };
}

export default async function CheckoutFailedPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);

  return (
    <div className="container mx-auto px-4 py-16 text-center max-w-lg">
      <div className="glass-card p-8 md:p-12">
        <XCircle className="h-16 w-16 text-destructive mx-auto mb-4" />
        <h1 className="text-2xl md:text-3xl font-bold">{t.checkout.failed.title}</h1>
        <p className="text-muted-foreground mt-2">{t.checkout.failed.subtitle}</p>
        <div className="flex flex-col sm:flex-row gap-3 mt-8 justify-center">
          <Button variant="gradient" asChild>
            <Link href={`/${locale}/checkout`}>{t.checkout.failed.retry}</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href={`/${locale}/cart`}>{t.common.cart}</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
