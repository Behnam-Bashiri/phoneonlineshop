import type { Locale } from "@/lib/i18n";
import en from "@/locales/en.json";
import fa from "@/locales/fa.json";

const translations = { en, fa } as const;

export function getTranslation(locale: Locale) {
  return translations[locale];
}

export type TranslationDict = typeof en;
