import type { Metadata } from "next";
import { WalletPage } from "@/components/account/wallet-page";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).account.wallet };
}

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return <WalletPage locale={locale as Locale} />;
}
