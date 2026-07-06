"use client";

import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, useCallback } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SafeImage } from "@/components/common/safe-image";
import { localeDirections } from "@/lib/i18n";
import type { HeroSlide } from "@/types";
import type { Locale } from "@/lib/i18n";

interface HeroSliderProps {
  slides: HeroSlide[];
  locale: Locale;
}

export function HeroSlider({ slides, locale }: HeroSliderProps) {
  const [current, setCurrent] = useState(0);
  const isRtl = localeDirections[locale] === "rtl";

  const next = useCallback(() => {
    setCurrent((c) => (c + 1) % slides.length);
  }, [slides.length]);

  const prev = useCallback(() => {
    setCurrent((c) => (c - 1 + slides.length) % slides.length);
  }, [slides.length]);

  useEffect(() => {
    const timer = setInterval(next, 6000);
    return () => clearInterval(timer);
  }, [next]);

  const slide = slides[current];
  const PrevIcon = isRtl ? ChevronRight : ChevronLeft;
  const NextIcon = isRtl ? ChevronLeft : ChevronRight;

  return (
    <section className="relative h-[50vh] md:h-[65vh] lg:h-[75vh] overflow-hidden rounded-3xl mx-4 md:mx-0">
      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, scale: 1.05 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.7 }}
          className="absolute inset-0"
        >
          <SafeImage
            src={slide.image}
            alt={slide.title}
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 hero-gradient" />
        </motion.div>
      </AnimatePresence>

      <div className="relative z-10 h-full container mx-auto px-8 flex flex-col justify-center">
        <motion.div
          key={`content-${current}`}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="max-w-xl text-start"
        >
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-white tracking-tight">
            {slide.title}
          </h1>
          <p className="mt-4 text-lg md:text-xl text-white/80">{slide.subtitle}</p>
          <Button variant="gradient" size="lg" className="mt-8" asChild>
            <Link href={`/${locale}${slide.link}`}>{slide.button_text}</Link>
          </Button>
        </motion.div>
      </div>

      <div className="absolute bottom-6 start-1/2 -translate-x-1/2 flex gap-2 z-10">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`h-2 rounded-full transition-all ${
              i === current ? "w-8 bg-white" : "w-2 bg-white/40"
            }`}
          />
        ))}
      </div>

      <Button
        variant="glass"
        size="icon"
        className="absolute start-4 top-1/2 -translate-y-1/2 z-10 rounded-full hidden md:flex"
        onClick={prev}
      >
        <PrevIcon className="h-5 w-5" />
      </Button>
      <Button
        variant="glass"
        size="icon"
        className="absolute end-4 top-1/2 -translate-y-1/2 z-10 rounded-full hidden md:flex"
        onClick={next}
      >
        <NextIcon className="h-5 w-5" />
      </Button>
    </section>
  );
}
