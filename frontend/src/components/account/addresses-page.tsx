"use client";

import { MapPin, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockAddresses = [
  { id: 1, title: "Home", full_name: "John Doe", address: "123 Main St, San Francisco, CA 94102", is_default: true },
  { id: 2, title: "Office", full_name: "John Doe", address: "456 Market St, San Francisco, CA 94103", is_default: false },
];

export function AddressesPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.addresses}</h1>
        <Button variant="gradient" size="sm"><Plus className="h-4 w-4 mr-1" /> Add</Button>
      </div>
      <div className="space-y-4">
        {mockAddresses.map((addr) => (
          <div key={addr.id} className="glass-card p-4 md:p-6">
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <MapPin className="h-5 w-5 text-blue-600 mt-0.5" />
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-semibold">{addr.title}</p>
                    {addr.is_default && <Badge variant="success">Default</Badge>}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{addr.full_name}</p>
                  <p className="text-sm mt-1">{addr.address}</p>
                </div>
              </div>
              <Button variant="ghost" size="sm">{t.common.edit}</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
