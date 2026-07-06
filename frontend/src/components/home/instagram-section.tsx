"use client";

import { Instagram } from "lucide-react";
import { SectionHeader } from "@/components/common/section-header";
import { FadeIn } from "@/components/common/motion-wrapper";
import { SafeImage } from "@/components/common/safe-image";
import type { Locale } from "@/lib/i18n";

const instagramImages = [
  "/images/products/iphone-16-pro-max.svg",
  "/images/products/google-pixel-9-pro.svg",
  "/images/products/samsung-galaxy-s25-ultra.svg",
  "/images/products/airpods-pro-3.svg",
  "/images/products/oneplus-13.svg",
  "/images/products/xiaomi-15-ultra.svg",
];

interface InstagramSectionProps {
  title: string;
  locale: Locale;
}

export function InstagramSection({ title }: InstagramSectionProps) {
  return (
    <section className="py-12 md:py-16 gradient-bg">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" subtitle="@phonyshop" />
        <div className="grid grid-cols-3 md:grid-cols-6 gap-2 md:gap-3">
          {instagramImages.map((src, i) => (
            <FadeIn key={i} delay={i * 0.05}>
              <a
                href="#"
                className="group relative aspect-square overflow-hidden rounded-xl"
              >
                <SafeImage
                  src={src}
                  alt={`Instagram ${i + 1}`}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors flex items-center justify-center">
                  <Instagram className="h-6 w-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </a>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
