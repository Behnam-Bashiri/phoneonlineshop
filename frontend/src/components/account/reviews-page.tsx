"use client";

import { Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useMockUserData } from "@/hooks/use-mock-user-data";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";

export function ReviewsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const data = useMockUserData(locale);
  const reviews = data?.reviews ?? [];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.reviews}</h1>
      {reviews.length === 0 ? (
        <p className="text-muted-foreground">
          {locale === "fa" ? "نظری ثبت نشده است." : "No reviews yet."}
        </p>
      ) : (
        <div className="space-y-4">
          {reviews.map((review) => (
            <div key={review.id} className="glass-card p-4 md:p-6">
              <div className="flex items-center justify-between mb-2">
                <p className="font-semibold text-sm">{review.productName}</p>
                <Badge variant="success">{t.common.verified}</Badge>
              </div>
              <div className="flex gap-0.5 mb-2">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={`h-4 w-4 ${
                      i < review.rating ? "fill-amber-400 text-amber-400" : "text-muted"
                    }`}
                  />
                ))}
              </div>
              <p className="font-medium text-sm">{review.title}</p>
              <p className="text-sm text-muted-foreground mt-1">{review.comment}</p>
              <p className="text-xs text-muted-foreground mt-2">
                {formatDate(review.created_at, locale)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
