"use client";

import Image from "next/image";
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
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12 opacity-60">
          {partners.map((partner, i) => (
            <FadeIn key={partner.id} delay={i * 0.05}>
              <div className="grayscale hover:grayscale-0 transition-all duration-300">
                <Image
                  src={partner.logo}
                  alt={partner.name}
                  width={120}
                  height={40}
                  className="object-contain h-8 md:h-10 w-auto dark:invert"
                />
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
