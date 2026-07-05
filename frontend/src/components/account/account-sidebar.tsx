"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  User,
  ShoppingBag,
  Wallet,
  Heart,
  MapPin,
  Ticket,
  Bell,
  MessageSquare,
  Star,
  Crown,
  Shield,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/hooks/use-translation";

interface AccountSidebarProps {
  locale: Locale;
}

export function AccountSidebar({ locale }: AccountSidebarProps) {
  const pathname = usePathname();
  const t = getTranslation(locale);

  const links = [
    { href: `/${locale}/account`, label: t.account.dashboard, icon: LayoutDashboard, exact: true },
    { href: `/${locale}/account/profile`, label: t.account.profile, icon: User },
    { href: `/${locale}/account/orders`, label: t.account.orders, icon: ShoppingBag },
    { href: `/${locale}/account/wallet`, label: t.account.wallet, icon: Wallet },
    { href: `/${locale}/account/favorites`, label: t.account.favorites, icon: Heart },
    { href: `/${locale}/account/addresses`, label: t.account.addresses, icon: MapPin },
    { href: `/${locale}/account/coupons`, label: t.account.coupons, icon: Ticket },
    { href: `/${locale}/account/notifications`, label: t.account.notifications, icon: Bell },
    { href: `/${locale}/account/tickets`, label: t.account.tickets, icon: MessageSquare },
    { href: `/${locale}/account/reviews`, label: t.account.reviews, icon: Star },
    { href: `/${locale}/account/club`, label: t.account.club, icon: Crown },
    { href: `/${locale}/account/security`, label: t.account.security, icon: Shield },
  ];

  return (
    <nav className="space-y-1">
      {links.map(({ href, label, icon: Icon, exact }) => {
        const isActive = exact
          ? pathname === href
          : pathname === href || pathname.startsWith(`${href}/`);

        return (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium transition-colors",
              isActive
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
