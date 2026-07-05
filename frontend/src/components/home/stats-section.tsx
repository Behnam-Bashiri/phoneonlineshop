"use client";

import { FadeIn } from "@/components/common/motion-wrapper";
import { getLucideIcon } from "@/lib/icons";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

interface StatsSectionProps {
  stats: { label: string; value: string; icon: string }[];
  locale: Locale;
}

export function StatsSection({ stats, locale }: StatsSectionProps) {
  const t = getTranslation(locale);

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, i) => {
            const IconComponent = getLucideIcon(stat.icon);
            const label =
              t.home.stats[stat.label as keyof typeof t.home.stats] || stat.label;
            return (
              <FadeIn key={stat.label} delay={i * 0.1}>
                <div className="text-center glass-card p-6 md:p-8">
                  <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center mx-auto mb-3">
                    <IconComponent className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="text-2xl md:text-3xl font-bold gradient-text">
                    {stat.value}
                  </div>
                  <div className="text-sm text-muted-foreground mt-1">{label}</div>
                </div>
              </FadeIn>
            );
          })}
        </div>
      </div>
    </section>
  );
}
