"use client";

import Link from "next/link";
import {
  ShoppingBag,
  Heart,
  MapPin,
  Wallet,
  Package,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/stores/auth-store";
import { formatPrice, formatDate } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockOrders = [
  {
    id: 1,
    order_number: "PS-20250601",
    status: "delivered" as const,
    total: 1199,
    created_at: "2025-06-01T00:00:00Z",
  },
  {
    id: 2,
    order_number: "PS-20250515",
    status: "shipped" as const,
    total: 249,
    created_at: "2025-05-15T00:00:00Z",
  },
];

export function AccountDashboard({ locale }: { locale: Locale }) {
  const { user } = useAuthStore();
  const t = getTranslation(locale);
  const name = user?.first_name || "Guest";

  const quickActions = [
    { href: `/${locale}/account/orders`, icon: ShoppingBag, label: t.account.orders },
    { href: `/${locale}/account/favorites`, icon: Heart, label: t.account.favorites },
    { href: `/${locale}/account/addresses`, icon: MapPin, label: t.account.addresses },
    { href: `/${locale}/account/wallet`, icon: Wallet, label: t.account.wallet },
  ];

  return (
    <div>
      <h1 className="text-2xl md:text-3xl font-bold mb-2">
        {t.account.welcomeBack.replace("{{name}}", name)}
      </h1>
      <p className="text-muted-foreground mb-8">{t.account.quickActions}</p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {quickActions.map(({ href, icon: Icon, label }) => (
          <Link key={href} href={href}>
            <Card className="glass-card hover:shadow-lg transition-shadow cursor-pointer h-full">
              <CardContent className="p-4 flex flex-col items-center text-center">
                <Icon className="h-8 w-8 text-blue-600 mb-2" />
                <span className="text-sm font-medium">{label}</span>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle>{t.account.recentOrders}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {mockOrders.map((order) => (
              <div
                key={order.id}
                className="flex items-center justify-between p-4 rounded-xl bg-muted/50"
              >
                <div className="flex items-center gap-3">
                  <Package className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="font-medium text-sm">{order.order_number}</p>
                    <p className="text-xs text-muted-foreground">
                      {formatDate(order.created_at, locale)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge
                    variant={
                      order.status === "delivered" ? "success" : "secondary"
                    }
                  >
                    {order.status}
                  </Badge>
                  <p className="text-sm font-semibold mt-1">
                    {formatPrice(order.total, locale)}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <Button variant="outline" className="w-full mt-4" asChild>
            <Link href={`/${locale}/account/orders`}>{t.common.viewAll}</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
