"use client";

import { Info, CheckCircle, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

const icons = {
  info: Info,
  success: CheckCircle,
  warning: AlertTriangle,
  error: AlertTriangle,
};

export function NotificationsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const notifications = data?.notifications ?? [];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.notifications}</h1>
        <Button variant="outline" size="sm">
          {locale === "fa" ? "خواندن همه" : "Mark all read"}
        </Button>
      </div>
      <div className="space-y-3">
        {notifications.map((notif) => {
          const Icon = icons[notif.type];
          return (
            <div
              key={notif.id}
              className={`glass-card p-4 flex gap-3 ${
                !notif.is_read ? "border-s-4 border-s-blue-600" : ""
              }`}
            >
              <Icon className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium text-sm">{notif.title}</p>
                  {!notif.is_read && (
                    <Badge variant="secondary" className="text-[10px]">
                      {locale === "fa" ? "جدید" : "New"}
                    </Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground mt-1">{notif.message}</p>
                <p className="text-xs text-muted-foreground mt-2">
                  {formatDate(notif.created_at, locale)}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
