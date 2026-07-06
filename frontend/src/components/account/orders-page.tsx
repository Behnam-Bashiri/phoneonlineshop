"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { formatPrice, formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

const statusLabels: Record<Locale, Record<string, string>> = {
  en: {
    delivered: "Delivered",
    shipped: "Shipped",
    processing: "Processing",
    pending: "Pending",
    cancelled: "Cancelled",
  },
  fa: {
    delivered: "تحویل شده",
    shipped: "ارسال شده",
    processing: "در حال پردازش",
    pending: "در انتظار",
    cancelled: "لغو شده",
  },
};

export function OrdersPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const orders = data?.orders ?? [];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.orders}</h1>
      {orders.length === 0 ? (
        <p className="text-muted-foreground">
          {locale === "fa" ? "سفارشی یافت نشد." : "No orders found."}
        </p>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="glass-card p-4 md:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div>
                <p className="font-semibold">{order.order_number}</p>
                <p className="text-sm text-muted-foreground">
                  {formatDate(order.created_at, locale)}
                  {order.tracking_number &&
                    ` · ${locale === "fa" ? "پیگیری" : "Tracking"}: ${order.tracking_number}`}
                </p>
              </div>
              <div className="flex items-center gap-4">
                <Badge
                  variant={order.status === "delivered" ? "success" : "secondary"}
                >
                  {statusLabels[locale][order.status] ?? order.status}
                </Badge>
                <span className="font-bold">{formatPrice(order.total, locale)}</span>
                <Button variant="outline" size="sm">
                  {locale === "fa" ? "جزئیات" : "Details"}
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
