"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/common/section-header";
import { FadeIn } from "@/components/common/motion-wrapper";
import { useCountdown } from "@/hooks/use-countdown";
import type { Offer } from "@/types";
import type { Locale } from "@/lib/i18n";

interface OffersSectionProps {
  offers: Offer[];
  locale: Locale;
  title: string;
}

export function OffersSection({ offers, locale, title }: OffersSectionProps) {
  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <div className="grid md:grid-cols-2 gap-6">
          {offers.map((offer, i) => (
            <FadeIn key={offer.id} delay={i * 0.1}>
              <OfferCard offer={offer} locale={locale} />
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

function OfferCard({ offer, locale }: { offer: Offer; locale: Locale }) {
  const countdown = useCountdown(offer.end_date);

  return (
    <Link href={`/${locale}${offer.link}`}>
      <div className="group relative overflow-hidden rounded-3xl h-64 md:h-72">
        <Image
          src={offer.image}
          alt={offer.title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-700"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
        <div className="absolute inset-0 p-6 flex flex-col justify-end">
          <Badge variant="destructive" className="w-fit mb-2">
            -{offer.discount}% OFF
          </Badge>
          <h3 className="text-2xl font-bold text-white">{offer.title}</h3>
          <p className="text-white/70 text-sm mt-1">{offer.description}</p>
          {!countdown.expired && (
            <div className="flex gap-3 mt-4">
              {[
                { label: "Days", value: countdown.days },
                { label: "Hrs", value: countdown.hours },
                { label: "Min", value: countdown.minutes },
                { label: "Sec", value: countdown.seconds },
              ].map(({ label, value }) => (
                <div
                  key={label}
                  className="glass rounded-xl px-3 py-2 text-center min-w-[52px]"
                >
                  <div className="text-lg font-bold text-white">
                    {String(value).padStart(2, "0")}
                  </div>
                  <div className="text-[10px] text-white/60">{label}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}

interface CountdownBannerProps {
  endDate: string;
  title: string;
  locale: Locale;
}

export function CountdownBanner({ endDate, title, locale }: CountdownBannerProps) {
  const countdown = useCountdown(endDate);

  if (countdown.expired) return null;

  return (
    <section className="py-8">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-8 md:p-12"
        >
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50" />
          <div className="relative flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold text-white">{title}</h2>
              <p className="text-white/80 mt-2">Don&apos;t miss out on exclusive deals</p>
            </div>
            <div className="flex gap-4">
              {[
                { label: "Days", value: countdown.days },
                { label: "Hours", value: countdown.hours },
                { label: "Minutes", value: countdown.minutes },
                { label: "Seconds", value: countdown.seconds },
              ].map(({ label, value }) => (
                <div
                  key={label}
                  className="bg-white/10 backdrop-blur-sm rounded-2xl px-4 py-3 text-center min-w-[70px]"
                >
                  <div className="text-2xl md:text-3xl font-bold text-white">
                    {String(value).padStart(2, "0")}
                  </div>
                  <div className="text-xs text-white/60 mt-1">{label}</div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
