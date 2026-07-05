"use client";

import { Info, CheckCircle, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockNotifications = [
  { id: 1, title: "Order Shipped", message: "Your order PS-20250515 has been shipped.", type: "success" as const, is_read: false, created_at: "2025-06-02T00:00:00Z" },
  { id: 2, title: "Flash Sale", message: "Summer sale is live! Up to 30% off.", type: "info" as const, is_read: false, created_at: "2025-06-01T00:00:00Z" },
  { id: 3, title: "Payment Received", message: "Payment for order PS-20250601 confirmed.", type: "success" as const, is_read: true, created_at: "2025-05-28T00:00:00Z" },
];

const icons = { info: Info, success: CheckCircle, warning: AlertTriangle, error: AlertTriangle };

export function NotificationsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.notifications}</h1>
        <Button variant="outline" size="sm">Mark all read</Button>
      </div>
      <div className="space-y-3">
        {mockNotifications.map((notif) => {
          const Icon = icons[notif.type];
          return (
            <div key={notif.id} className={`glass-card p-4 flex gap-3 ${!notif.is_read ? "border-l-4 border-l-blue-600" : ""}`}>
              <Icon className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium text-sm">{notif.title}</p>
                  {!notif.is_read && <Badge variant="secondary" className="text-[10px]">New</Badge>}
                </div>
                <p className="text-sm text-muted-foreground mt-1">{notif.message}</p>
                <p className="text-xs text-muted-foreground mt-2">{formatDate(notif.created_at, locale)}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
