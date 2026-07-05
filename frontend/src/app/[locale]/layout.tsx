import { notFound } from "next/navigation";
import { Providers } from "@/components/common/providers";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { locales, localeDirections, isValidLocale, type Locale } from "@/lib/i18n";

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  if (!isValidLocale(locale)) {
    notFound();
  }

  const direction = localeDirections[locale as Locale];

  return (
    <div lang={locale} dir={direction}>
      <Providers>
        <div className="flex min-h-screen flex-col">
          <Header locale={locale as Locale} />
          <main className="flex-1">{children}</main>
          <Footer locale={locale as Locale} />
        </div>
      </Providers>
    </div>
  );
}
