"use client";

import Link from "next/link";
import { useState } from "react";
import {
  Search,
  ShoppingCart,
  Heart,
  Menu,
  User,
  Smartphone,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { ThemeToggle } from "@/components/common/theme-toggle";
import { LocaleSwitcher } from "@/components/common/locale-switcher";
import { useCartStore } from "@/stores/cart-store";
import { useWishlistStore } from "@/stores/wishlist-store";
import { useAuthStore } from "@/stores/auth-store";
import { cn } from "@/lib/utils";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/hooks/use-translation";

interface HeaderProps {
  locale: Locale;
}

export function Header({ locale }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const cartCount = useCartStore((s) => s.getItemCount());
  const wishlistCount = useWishlistStore((s) => s.items.length);
  const { isAuthenticated, user, logout } = useAuthStore();
  const t = getTranslation(locale);
  const isRtl = locale === "fa";

  const navLinks = [
    { href: `/${locale}/products`, label: t.common.products },
    { href: `/${locale}/blog`, label: t.common.blog },
    { href: `/${locale}/contact`, label: t.common.contact },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/${locale}/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <header className="sticky top-0 z-50 glass border-b">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between gap-4">
          <Link
            href={`/${locale}`}
            className="flex items-center gap-2 font-bold text-xl shrink-0"
          >
            <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
              <Smartphone className="h-4 w-4 text-white" />
            </div>
            <span className="gradient-text hidden sm:inline">{t.common.siteName}</span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <form
            onSubmit={handleSearch}
            className={cn(
              "flex-1 max-w-md hidden lg:flex items-center relative",
              searchOpen && "flex"
            )}
          >
            <Search className="absolute start-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder={t.common.searchPlaceholder}
              className="ps-10 rounded-full bg-muted/50"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>

          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden rounded-full"
              onClick={() => setSearchOpen(!searchOpen)}
            >
              <Search className="h-5 w-5" />
            </Button>

            <ThemeToggle locale={locale} />
            <LocaleSwitcher currentLocale={locale} />

            <Link href={`/${locale}/wishlist`}>
              <Button variant="ghost" size="icon" className="rounded-full relative">
                <Heart className="h-5 w-5" />
                {wishlistCount > 0 && (
                  <Badge className="absolute -top-1 -end-1 h-5 w-5 p-0 flex items-center justify-center text-[10px]">
                    {wishlistCount}
                  </Badge>
                )}
              </Button>
            </Link>

            <Link href={`/${locale}/cart`}>
              <Button variant="ghost" size="icon" className="rounded-full relative">
                <ShoppingCart className="h-5 w-5" />
                {cartCount > 0 && (
                  <Badge className="absolute -top-1 -end-1 h-5 w-5 p-0 flex items-center justify-center text-[10px]">
                    {cartCount}
                  </Badge>
                )}
              </Button>
            </Link>

            {isAuthenticated ? (
              <Link href={`/${locale}/account`}>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <User className="h-5 w-5" />
                </Button>
              </Link>
            ) : (
              <Link href={`/${locale}/auth/login`} className="hidden sm:block">
                <Button variant="gradient" size="sm">
                  {t.common.login}
                </Button>
              </Link>
            )}

            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden rounded-full">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side={isRtl ? "left" : "right"}>
                <SheetHeader>
                  <SheetTitle>{t.common.siteName}</SheetTitle>
                </SheetHeader>
                <nav className="flex flex-col gap-4 mt-8">
                  {navLinks.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      className="text-lg font-medium"
                    >
                      {link.label}
                    </Link>
                  ))}
                  <Link href={`/${locale}/compare`} className="text-lg font-medium">
                    {t.common.compare}
                  </Link>
                  {isAuthenticated ? (
                    <>
                      <Link href={`/${locale}/account`} className="text-lg font-medium">
                        {t.common.account}
                      </Link>
                      <Button variant="outline" onClick={logout}>
                        {t.common.logout}
                      </Button>
                    </>
                  ) : (
                    <Link href={`/${locale}/auth/login`}>
                      <Button variant="gradient" className="w-full">
                        {t.common.login}
                      </Button>
                    </Link>
                  )}
                </nav>
              </SheetContent>
            </Sheet>
          </div>
        </div>

        {searchOpen && (
          <form onSubmit={handleSearch} className="lg:hidden pb-3 relative">
            <Search className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder={t.common.searchPlaceholder}
              className="ps-10 rounded-full"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              autoFocus
            />
          </form>
        )}
      </div>
    </header>
  );
}
