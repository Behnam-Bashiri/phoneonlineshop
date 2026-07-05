"use client";

import { SectionHeader } from "@/components/common/section-header";
import { FadeIn } from "@/components/common/motion-wrapper";
import { getLucideIcon } from "@/lib/icons";
import type { Advantage } from "@/types";

interface AdvantagesSectionProps {
  advantages: Advantage[];
  title: string;
}

export function AdvantagesSection({ advantages, title }: AdvantagesSectionProps) {
  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {advantages.map((adv, i) => {
            const IconComponent = getLucideIcon(adv.icon);
            return (
              <FadeIn key={adv.id} delay={i * 0.1}>
                <div className="text-center p-4">
                  <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-blue-500/20">
                    <IconComponent className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="font-semibold">{adv.title}</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    {adv.description}
                  </p>
                </div>
              </FadeIn>
            );
          })}
        </div>
      </div>
    </section>
  );
}
