"use client";

import { Ticket, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { formatDate, formatPrice } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export function CouponsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const coupons = data?.coupons ?? [];

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    toast({
      title: t.toast.copied,
      description: code,
    });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.coupons}</h1>
      {coupons.length === 0 ? (
        <p className="text-muted-foreground">
          {locale === "fa" ? "کد تخفیفی موجود نیست." : "No coupons available."}
        </p>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {coupons.map((coupon) => (
            <div key={coupon.id} className="glass-card p-6 border-dashed border-2">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Ticket className="h-5 w-5 text-blue-600" />
                  <span className="font-mono font-bold text-lg">{coupon.code}</span>
                </div>
                <Badge variant="success">
                  {coupon.discount_type === "percentage"
                    ? `${coupon.discount_value}%`
                    : formatPrice(coupon.discount_value, locale)}{" "}
                  {t.common.off}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                {locale === "fa" ? "حداقل سفارش" : "Min order"}:{" "}
                {formatPrice(coupon.min_order, locale)}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                {locale === "fa" ? "انقضا" : "Expires"}:{" "}
                {formatDate(coupon.expires_at, locale)}
              </p>
              <Button
                variant="outline"
                size="sm"
                className="mt-3"
                onClick={() => copyCode(coupon.code)}
              >
                <Copy className="h-3 w-3 me-1" />
                {locale === "fa" ? "کپی" : "Copy"}
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
