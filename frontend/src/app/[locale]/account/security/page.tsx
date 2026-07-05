import type { Metadata } from "next";
import { SecurityPage } from "@/components/account/security-page";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).account.security };
}

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return <SecurityPage locale={locale as Locale} />;
}
