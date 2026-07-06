"use client";

import { useEffect } from "react";
import type { Locale } from "@/lib/i18n";
import { localeDirections } from "@/lib/i18n";

interface LocaleAttributesProps {
  locale: Locale;
}

/** Syncs `lang` and `dir` on the document root for RTL/LTR and portals. */
export function LocaleAttributes({ locale }: LocaleAttributesProps) {
  const direction = localeDirections[locale];

  useEffect(() => {
    document.documentElement.lang = locale;
    document.documentElement.dir = direction;
    document.body.dataset.locale = locale;
    document.body.dataset.direction = direction;
  }, [locale, direction]);

  return null;
}
