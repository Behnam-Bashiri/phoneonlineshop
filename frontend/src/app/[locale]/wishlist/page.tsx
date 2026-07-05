import type { Metadata } from "next";
import { WishlistPageContent } from "@/components/product/wishlist-page";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).wishlist.title };
}

export default async function WishlistPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return <WishlistPageContent locale={locale as Locale} />;
}
