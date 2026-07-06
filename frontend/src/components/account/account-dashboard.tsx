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

export function AccountDashboard({ locale }: { locale: Locale }) {
  const { user } = useAuthStore();
  const data = useMockUserData(locale);
  const t = getTranslation(locale);
  const name = user?.first_name || (locale === "fa" ? "مهمان" : "Guest");
  const orders = data?.orders.slice(0, 2) ?? [];

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
      {user?.role === "admin" && (
        <Badge variant="secondary" className="mb-4">
          {locale === "fa" ? "مدیر سیستم" : "Administrator"}
        </Badge>
      )}
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

      {orders.length > 0 ? (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>{t.account.recentOrders}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {orders.map((order) => (
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
                  <div className="text-end">
                    <Badge
                      variant={
                        order.status === "delivered" ? "success" : "secondary"
                      }
                    >
                      {statusLabels[locale][order.status] ?? order.status}
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
      ) : (
        <Card className="glass-card p-6 text-center text-muted-foreground">
          {locale === "fa"
            ? "پنل مدیریت — از منوی Django Admin برای مدیریت فروشگاه استفاده کنید."
            : "Admin panel — use Django Admin to manage the store."}
        </Card>
      )}
    </div>
  );
}
