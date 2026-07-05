import type { Metadata } from "next";
import { AccountDashboard } from "@/components/account/account-dashboard";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = getTranslation(locale as Locale);
  return { title: t.account.dashboard };
}

export default async function AccountPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  return <AccountDashboard locale={locale as Locale} />;
}
