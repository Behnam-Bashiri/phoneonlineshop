import type { Metadata } from "next";
import { ContactPageContent } from "@/components/common/contact-page";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).contact.title };
}

export default async function ContactPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return <ContactPageContent locale={locale as Locale} />;
}
