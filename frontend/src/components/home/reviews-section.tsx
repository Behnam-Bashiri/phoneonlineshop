"use client";

import { Star } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { SectionHeader } from "@/components/common/section-header";
import { getInitials, formatDate } from "@/lib/utils";
import type { Review } from "@/types";
import type { Locale } from "@/lib/i18n";

interface ReviewsSectionProps {
  reviews: Review[];
  locale: Locale;
  title: string;
}

export function ReviewsSection({ reviews, locale, title }: ReviewsSectionProps) {
  return (
    <section className="py-12 md:py-16 gradient-bg">
      <div className="container mx-auto px-4">
        <SectionHeader title={title} align="center" />
        <Carousel opts={{ align: "start", loop: true }} className="mx-auto max-w-5xl">
          <CarouselContent className="-ml-4">
            {reviews.map((review) => (
              <CarouselItem key={review.id} className="pl-4 md:basis-1/2 lg:basis-1/3">
                <Card className="glass-card h-full">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-4">
                      <Avatar>
                        <AvatarFallback>{getInitials(review.user.name)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-medium text-sm">{review.user.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {formatDate(review.created_at, locale)}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-0.5 mb-3">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`h-4 w-4 ${
                            i < review.rating
                              ? "fill-amber-400 text-amber-400"
                              : "text-muted"
                          }`}
                        />
                      ))}
                    </div>
                    <h4 className="font-semibold text-sm mb-1">{review.title}</h4>
                    <p className="text-sm text-muted-foreground line-clamp-3">
                      {review.comment}
                    </p>
                  </CardContent>
                </Card>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="hidden md:flex -left-12" />
          <CarouselNext className="hidden md:flex -right-12" />
        </Carousel>
      </div>
    </section>
  );
}
