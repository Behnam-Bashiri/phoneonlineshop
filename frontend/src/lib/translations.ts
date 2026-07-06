import type { Locale } from "@/lib/i18n";
import en from "@/locales/en.json";
import fa from "@/locales/fa.json";

const translations = { en, fa } as const;

export function getTranslation(locale: Locale) {
  return translations[locale];
}

export type TranslationDict = typeof en;

/** Resolve dot-notation key with optional {{param}} interpolation */
export function translate(
  locale: Locale,
  key: string,
  params?: Record<string, string | number>
): string {
  const keys = key.split(".");
  let value: unknown = translations[locale];
  for (const k of keys) {
    value = (value as Record<string, unknown>)?.[k];
  }
  if (typeof value !== "string") return key;
  if (!params) return value;
  return Object.entries(params).reduce(
    (str, [k, v]) => str.replaceAll(`{{${k}}}`, String(v)),
    value
  );
}
