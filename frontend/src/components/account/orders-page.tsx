"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatPrice, formatDate } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockOrders = [
  { id: 1, order_number: "PS-20250601", status: "delivered", total: 1199, items: 1, created_at: "2025-06-01T00:00:00Z" },
  { id: 2, order_number: "PS-20250515", status: "shipped", total: 249, items: 1, created_at: "2025-05-15T00:00:00Z" },
  { id: 3, order_number: "PS-20250420", status: "processing", total: 1099, items: 1, created_at: "2025-04-20T00:00:00Z" },
];

export function OrdersPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.orders}</h1>
      <div className="space-y-4">
        {mockOrders.map((order) => (
          <div key={order.id} className="glass-card p-4 md:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <p className="font-semibold">{order.order_number}</p>
              <p className="text-sm text-muted-foreground">{formatDate(order.created_at, locale)} · {order.items} item(s)</p>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant={order.status === "delivered" ? "success" : "secondary"}>{order.status}</Badge>
              <span className="font-bold">{formatPrice(order.total, locale)}</span>
              <Button variant="outline" size="sm">Details</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
