"use client";

import { MessageSquare, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockTickets = [
  { id: 1, subject: "Order delivery delay", category: "Orders", status: "open" as const, priority: "high" as const, created_at: "2025-06-01T00:00:00Z" },
  { id: 2, subject: "Product warranty question", category: "Products", status: "resolved" as const, priority: "low" as const, created_at: "2025-05-20T00:00:00Z" },
];

export function TicketsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t.account.tickets}</h1>
        <Button variant="gradient" size="sm"><Plus className="h-4 w-4 mr-1" /> New Ticket</Button>
      </div>
      <div className="space-y-4">
        {mockTickets.map((ticket) => (
          <div key={ticket.id} className="glass-card p-4 md:p-6 flex items-center justify-between gap-4 cursor-pointer hover:shadow-lg transition-shadow">
            <div className="flex items-center gap-3">
              <MessageSquare className="h-5 w-5 text-blue-600" />
              <div>
                <p className="font-semibold text-sm">{ticket.subject}</p>
                <p className="text-xs text-muted-foreground">{ticket.category} · {formatDate(ticket.created_at, locale)}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant={ticket.status === "open" ? "warning" : "success"}>{ticket.status}</Badge>
              <Badge variant="outline">{ticket.priority}</Badge>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
