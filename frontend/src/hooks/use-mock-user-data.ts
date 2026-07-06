"use client";

import { useAuthStore } from "@/stores/auth-store";
import { getMockUserAccountData } from "@/lib/mock-users";
import type { Locale } from "@/lib/i18n";

export function useMockUserData(locale: Locale) {
  const user = useAuthStore((s) => s.user);
  return getMockUserAccountData(locale, user?.email);
}
