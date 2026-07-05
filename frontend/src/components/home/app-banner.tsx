"use client";

import { Smartphone, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { FadeIn } from "@/components/common/motion-wrapper";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/hooks/use-translation";

interface AppBannerProps {
  locale: Locale;
}

export function AppBanner({ locale }: AppBannerProps) {
  const t = getTranslation(locale);

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <FadeIn>
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-gray-900 to-gray-800 dark:from-gray-800 dark:to-gray-900 p-8 md:p-12">
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-purple-500/20 rounded-full blur-3xl" />
            <div className="relative flex flex-col md:flex-row items-center gap-8">
              <div className="flex-1 text-center md:text-left">
                <h2 className="text-2xl md:text-3xl font-bold text-white">
                  {t.home.appBanner.title}
                </h2>
                <p className="text-white/70 mt-2 mb-6">
                  {t.home.appBanner.subtitle}
                </p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center md:justify-start">
                  <Button variant="gradient" size="lg" className="rounded-full">
                    <Download className="mr-2 h-5 w-5" />
                    App Store
                  </Button>
                  <Button
                    variant="outline"
                    size="lg"
                    className="rounded-full border-white/20 text-white hover:bg-white/10"
                  >
                    <Download className="mr-2 h-5 w-5" />
                    Google Play
                  </Button>
                </div>
              </div>
              <div className="relative">
                <div className="h-48 w-48 md:h-64 md:w-64 rounded-3xl bg-gradient-to-br from-blue-600/30 to-purple-600/30 flex items-center justify-center">
                  <Smartphone className="h-24 w-24 md:h-32 md:w-32 text-white/80" />
                </div>
              </div>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
