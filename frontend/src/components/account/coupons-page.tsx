"use client";

import { Ticket, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockCoupons = [
  { id: 1, code: "SUMMER30", discount_type: "percentage" as const, discount_value: 30, min_order: 100, expires_at: "2025-08-01T00:00:00Z", is_active: true },
  { id: 2, code: "WELCOME10", discount_type: "fixed" as const, discount_value: 10, min_order: 50, expires_at: "2025-12-31T00:00:00Z", is_active: true },
];

export function CouponsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    toast({ title: "Copied!", description: code });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.coupons}</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {mockCoupons.map((coupon) => (
          <div key={coupon.id} className="glass-card p-6 border-dashed border-2">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Ticket className="h-5 w-5 text-blue-600" />
                <span className="font-mono font-bold text-lg">{coupon.code}</span>
              </div>
              <Badge variant="success">
                {coupon.discount_type === "percentage" ? `${coupon.discount_value}%` : `$${coupon.discount_value}`} OFF
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">Min order: ${coupon.min_order}</p>
            <p className="text-xs text-muted-foreground mt-1">Expires: {formatDate(coupon.expires_at, locale)}</p>
            <Button variant="outline" size="sm" className="mt-3" onClick={() => copyCode(coupon.code)}>
              <Copy className="h-3 w-3 mr-1" /> Copy
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
