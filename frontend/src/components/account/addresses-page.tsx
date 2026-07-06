"use client";

import { MapPin, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export function AddressesPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const addresses = data?.addresses ?? [];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.addresses}</h1>
        <Button variant="gradient" size="sm">
          <Plus className="h-4 w-4 me-1" />
          {locale === "fa" ? "افزودن" : "Add"}
        </Button>
      </div>
      <div className="space-y-4">
        {addresses.map((addr) => (
          <div key={addr.id} className="glass-card p-4 md:p-6">
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <MapPin className="h-5 w-5 text-blue-600 mt-0.5" />
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-semibold">{addr.title}</p>
                    {addr.is_default && (
                      <Badge variant="success">
                        {locale === "fa" ? "پیش‌فرض" : "Default"}
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    {addr.full_name} · {addr.phone}
                  </p>
                  <p className="text-sm mt-1">
                    {addr.province}، {addr.city} — {addr.address}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {locale === "fa" ? "کد پستی" : "Postal"}: {addr.postal_code}
                  </p>
                </div>
              </div>
              <Button variant="ghost" size="sm">
                {t.common.edit}
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
