import Link from "next/link";
import { Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { SafeImage } from "@/components/common/safe-image";
import { getMockBlogPosts } from "@/lib/mock-data";
import { formatDate } from "@/lib/utils";
import { getTranslation, translate } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";
import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return { title: getTranslation(locale as Locale).blog.title };
}

export default async function BlogPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const loc = locale as Locale;
  const t = getTranslation(loc);
  const mockBlogPosts = getMockBlogPosts(loc);

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <h1 className="text-3xl font-bold mb-8">{t.blog.title}</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockBlogPosts.map((post) => (
          <Link key={post.id} href={`/${locale}/blog/${post.slug}`}>
            <Card className="group overflow-hidden glass-card hover:shadow-xl transition-all h-full">
              <div className="relative aspect-[16/10] overflow-hidden">
                {post.image && (
                  <SafeImage src={post.image} alt={post.title} fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                )}
                <Badge className="absolute top-3 start-3">{post.category}</Badge>
              </div>
              <CardContent className="p-5">
                <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                  <Clock className="h-3 w-3" />
                  {translate(loc, "blog.readTime", { minutes: post.read_time })}
                  <span>·</span>
                  {formatDate(post.published_at, loc)}
                </div>
                <h2 className="font-semibold line-clamp-2 group-hover:text-blue-600 transition-colors">{post.title}</h2>
                <p className="text-sm text-muted-foreground mt-2 line-clamp-2">{post.excerpt}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
