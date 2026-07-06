"use client";

import { MessageSquare, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

const statusLabels: Record<Locale, Record<string, string>> = {
  en: {
    open: "Open",
    in_progress: "In Progress",
    resolved: "Resolved",
    closed: "Closed",
  },
  fa: {
    open: "باز",
    in_progress: "در حال بررسی",
    resolved: "حل شده",
    closed: "بسته",
  },
};

export function TicketsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const tickets = data?.tickets ?? [];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.tickets}</h1>
        <Button variant="gradient" size="sm">
          <Plus className="h-4 w-4 me-1" />
          {locale === "fa" ? "تیکت جدید" : "New Ticket"}
        </Button>
      </div>
      <div className="space-y-4">
        {tickets.map((ticket) => (
          <div
            key={ticket.id}
            className="glass-card p-4 md:p-6 flex items-center justify-between gap-4 cursor-pointer hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center gap-3">
              <MessageSquare className="h-5 w-5 text-blue-600" />
              <div>
                <p className="font-semibold text-sm">{ticket.subject}</p>
                <p className="text-xs text-muted-foreground">
                  {ticket.category} · {formatDate(ticket.created_at, locale)}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge
                variant={
                  ticket.status === "open" || ticket.status === "in_progress"
                    ? "warning"
                    : "success"
                }
              >
                {statusLabels[locale][ticket.status] ?? ticket.status}
              </Badge>
              <Badge variant="outline">{ticket.priority}</Badge>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
