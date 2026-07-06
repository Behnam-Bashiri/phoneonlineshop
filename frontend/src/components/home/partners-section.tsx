"use client";

import { SectionHeader } from "@/components/common/section-header";
import { FadeIn } from "@/components/common/motion-wrapper";
import type { Partner } from "@/types";

interface PartnersSectionProps {
  partners: Partner[];
  title: string;
}

export function PartnersSection({ partners, title }: PartnersSectionProps) {
  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <div className="flex flex-wrap items-center justify-center gap-6 md:gap-10">
          {partners.map((partner, i) => (
            <FadeIn key={partner.id} delay={i * 0.05}>
              <div className="glass-card px-8 py-4 rounded-2xl hover:shadow-lg transition-all">
                <span className="text-lg md:text-xl font-bold text-muted-foreground hover:text-foreground transition-colors">
                  {partner.name}
                </span>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
