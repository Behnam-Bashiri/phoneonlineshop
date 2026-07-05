"use client";

import Link from "next/link";
import Image from "next/image";
import { Clock } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/common/section-header";
import { ViewAllLink } from "@/components/common/view-all-link";
import { FadeIn } from "@/components/common/motion-wrapper";
import { formatDate } from "@/lib/utils";
import type { BlogPost } from "@/types";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/hooks/use-translation";

interface BlogSectionProps {
  posts: BlogPost[];
  locale: Locale;
  title: string;
}

export function BlogSection({ posts, locale, title }: BlogSectionProps) {
  const t = getTranslation(locale);

  return (
    <section className="py-12 md:py-16">
      <div className="container mx-auto px-4">
        <div className="flex items-end justify-between mb-8">
          <SectionHeader title={title} className="mb-0" />
          <ViewAllLink href={`/${locale}/blog`} label={t.common.viewAll} />
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {posts.map((post, i) => (
            <FadeIn key={post.id} delay={i * 0.1}>
              <Link href={`/${locale}/blog/${post.slug}`}>
                <Card className="group overflow-hidden glass-card hover:shadow-xl transition-all h-full">
                  <div className="relative aspect-[16/10] overflow-hidden">
                    {post.image && (
                      <Image
                        src={post.image}
                        alt={post.title}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    )}
                    <Badge className="absolute top-3 left-3">{post.category}</Badge>
                  </div>
                  <CardContent className="p-5">
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                      <Clock className="h-3 w-3" />
                      {t.blog.readTime.replace("{{minutes}}", String(post.read_time))}
                      <span>·</span>
                      {formatDate(post.published_at, locale)}
                    </div>
                    <h3 className="font-semibold line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {post.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                      {post.excerpt}
                    </p>
                  </CardContent>
                </Card>
              </Link>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
