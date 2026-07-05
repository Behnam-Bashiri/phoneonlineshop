"use client";

import { useState } from "react";
import { Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "@/hooks/use-toast";
import { FadeIn } from "@/components/common/motion-wrapper";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/hooks/use-translation";

interface NewsletterSectionProps {
  locale: Locale;
}

export function NewsletterSection({ locale }: NewsletterSectionProps) {
  const t = getTranslation(locale);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1000));
    toast({ title: "Subscribed!", description: "Thank you for subscribing." });
    setEmail("");
    setLoading(false);
  };

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <FadeIn>
          <div className="relative overflow-hidden rounded-3xl glass-card p-8 md:p-12 text-center max-w-3xl mx-auto">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5" />
            <div className="relative">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center mx-auto mb-4">
                <Mail className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl md:text-3xl font-bold">
                {t.home.newsletter.title}
              </h2>
              <p className="text-muted-foreground mt-2 mb-6">
                {t.home.newsletter.subtitle}
              </p>
              <form
                onSubmit={handleSubmit}
                className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto"
              >
                <Input
                  type="email"
                  placeholder={t.home.newsletter.placeholder}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="rounded-full"
                />
                <Button
                  type="submit"
                  variant="gradient"
                  disabled={loading}
                  className="rounded-full shrink-0"
                >
                  {t.home.newsletter.button}
                </Button>
              </form>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
