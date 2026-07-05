"use client";

import { Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

const mockReviews = [
  { id: 1, product: "iPhone 16 Pro Max", rating: 5, title: "Amazing phone!", comment: "Best purchase ever.", created_at: "2025-06-01T00:00:00Z", is_verified: true },
  { id: 2, product: "AirPods Pro 3", rating: 4, title: "Great sound", comment: "ANC is incredible.", created_at: "2025-05-15T00:00:00Z", is_verified: true },
];

export function ReviewsPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.reviews}</h1>
      <div className="space-y-4">
        {mockReviews.map((review) => (
          <div key={review.id} className="glass-card p-4 md:p-6">
            <div className="flex items-center justify-between mb-2">
              <p className="font-semibold text-sm">{review.product}</p>
              {review.is_verified && <Badge variant="success">Verified</Badge>}
            </div>
            <div className="flex gap-0.5 mb-2">
              {Array.from({ length: 5 }).map((_, i) => (
                <Star key={i} className={`h-4 w-4 ${i < review.rating ? "fill-amber-400 text-amber-400" : "text-muted"}`} />
              ))}
            </div>
            <p className="font-medium text-sm">{review.title}</p>
            <p className="text-sm text-muted-foreground mt-1">{review.comment}</p>
            <p className="text-xs text-muted-foreground mt-2">{formatDate(review.created_at, locale)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
