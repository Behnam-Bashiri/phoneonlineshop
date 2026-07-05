"use client";

import { useEffect, useState } from "react";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/lib/translations";

export function useTranslation(locale: Locale) {
  const [dict, setDict] = useState(getTranslation(locale));

  useEffect(() => {
    setDict(getTranslation(locale));
  }, [locale]);

  const t = (key: string, params?: Record<string, string | number>): string => {
    const keys = key.split(".");
    let value: unknown = dict;
    for (const k of keys) {
      value = (value as Record<string, unknown>)?.[k];
    }
    if (typeof value !== "string") return key;
    if (params) {
      return Object.entries(params).reduce(
        (str, [k, v]) => str.replace(`{{${k}}}`, String(v)),
        value
      );
    }
    return value;
  };

  return { t, dict };
}

export { getTranslation } from "@/lib/translations";
