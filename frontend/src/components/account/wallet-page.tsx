"use client";

import { Wallet, Plus, ArrowUpRight, ArrowDownLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { getWalletDisplayAmount } from "@/lib/mock-users";
import { formatPrice, formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export function WalletPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const balance = getWalletDisplayAmount(data?.walletBalance ?? 0, locale);
  const transactions = data?.walletTransactions ?? [];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.wallet}</h1>
      <div className="glass-card p-6 md:p-8 mb-6 bg-gradient-to-br from-blue-600 to-purple-600 text-white">
        <div className="flex items-center gap-3 mb-4">
          <Wallet className="h-6 w-6" />
          <span className="text-white/80">
            {locale === "fa" ? "موجودی" : "Balance"}
          </span>
        </div>
        <p className="text-4xl font-bold">{formatPrice(balance, locale)}</p>
        <Button variant="secondary" className="mt-4" size="sm">
          <Plus className="h-4 w-4 me-1" />
          {locale === "fa" ? "شارژ کیف پول" : "Top Up"}
        </Button>
      </div>
      <div className="space-y-3">
        {transactions.map((tx) => (
          <div key={tx.id} className="glass-card p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              {tx.type === "credit" ? (
                <ArrowDownLeft className="h-5 w-5 text-green-500" />
              ) : (
                <ArrowUpRight className="h-5 w-5 text-red-500" />
              )}
              <div>
                <p className="font-medium text-sm">{tx.description}</p>
                <p className="text-xs text-muted-foreground">
                  {formatDate(tx.created_at, locale)}
                </p>
              </div>
            </div>
            <Badge variant={tx.type === "credit" ? "success" : "destructive"}>
              {tx.type === "credit" ? "+" : "-"}
              {formatPrice(getWalletDisplayAmount(tx.amount, locale), locale)}
            </Badge>
          </div>
        ))}
      </div>
    </div>
  );
}
