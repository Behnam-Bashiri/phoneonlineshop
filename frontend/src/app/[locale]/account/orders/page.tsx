import type { Metadata } from "next";
import { OrdersPage } from "@/components/account/orders-page";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).account.orders };
}

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return <OrdersPage locale={locale as Locale} />;
}
