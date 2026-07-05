"use client";

import Image from "next/image";
import { Instagram } from "lucide-react";
import { SectionHeader } from "@/components/common/section-header";
import { FadeIn } from "@/components/common/motion-wrapper";

const instagramImages = [
  "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
  "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400",
  "https://images.unsplash.com/photo-1610945265064-0e34e5519dff?w=400",
  "https://images.unsplash.com/photo-1606841837239-b5d59190402e?w=400",
  "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",
  "https://images.unsplash.com/photo-1695048133142-1a204686a853?w=400",
];

interface InstagramSectionProps {
  title: string;
}

export function InstagramSection({ title }: InstagramSectionProps) {
  return (
    <section className="py-12 md:py-16 gradient-bg">
      <div className="container mx-auto px-4">
        <SectionHeader
          title={title}
          align="center"
          subtitle="@phonyshop"
        />
        <div className="grid grid-cols-3 md:grid-cols-6 gap-2 md:gap-3">
          {instagramImages.map((src, i) => (
            <FadeIn key={i} delay={i * 0.05}>
              <a
                href="#"
                className="group relative aspect-square overflow-hidden rounded-xl"
              >
                <Image
                  src={src}
                  alt={`Instagram post ${i + 1}`}
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
