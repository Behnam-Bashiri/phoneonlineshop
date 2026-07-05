"use client";

import { Crown, Gift, Star, TrendingUp } from "lucide-react";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function ClubPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const points = 2450;
  const tier = "Gold";
  const nextTier = 3000;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.club}</h1>
      <div className="glass-card p-6 md:p-8 mb-6 bg-gradient-to-br from-amber-500 to-orange-600 text-white">
        <div className="flex items-center gap-3 mb-4">
          <Crown className="h-8 w-8" />
          <div>
            <p className="text-white/80 text-sm">Membership Tier</p>
            <p className="text-2xl font-bold">{tier}</p>
          </div>
        </div>
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-2">
            <span>{points} points</span>
            <span>{nextTier} for Platinum</span>
          </div>
          <div className="h-2 bg-white/20 rounded-full overflow-hidden">
            <div className="h-full bg-white rounded-full" style={{ width: `${(points / nextTier) * 100}%` }} />
          </div>
        </div>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {[
          { icon: Gift, title: "Exclusive Offers", desc: "Member-only discounts" },
          { icon: Star, title: "Bonus Points", desc: "2x points on purchases" },
          { icon: TrendingUp, title: "Early Access", desc: "New products first" },
        ].map(({ icon: Icon, title, desc }) => (
          <div key={title} className="glass-card p-4 text-center">
            <Icon className="h-8 w-8 mx-auto text-amber-500 mb-2" />
            <p className="font-semibold text-sm">{title}</p>
            <p className="text-xs text-muted-foreground mt-1">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
