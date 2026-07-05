import { notFound } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { Clock, ArrowLeft } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getBlogPostBySlug, mockBlogPosts } from "@/lib/mock-data";
import { formatDate } from "@/lib/utils";
import { getTranslation } from "@/lib/translations";
import type { Locale } from "@/lib/i18n";
import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) return { title: "Not Found" };
  return { title: post.title, description: post.excerpt };
}

export function generateStaticParams() {
  return mockBlogPosts.map((p) => ({ slug: p.slug }));
}

export default async function BlogPostPage({ params }: { params: Promise<{ locale: string; slug: string }> }) {
  const { locale, slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) notFound();
  const t = getTranslation(locale as Locale);

  return (
    <article className="container mx-auto px-4 py-8 md:py-12 max-w-3xl">
      <Button variant="ghost" size="sm" asChild className="mb-6">
        <Link href={`/${locale}/blog`}><ArrowLeft className="h-4 w-4 mr-1" /> {t.common.back}</Link>
      </Button>
      {post.image && (
        <div className="relative aspect-[21/9] rounded-3xl overflow-hidden mb-8">
          <Image src={post.image} alt={post.title} fill className="object-cover" priority />
        </div>
      )}
      <Badge className="mb-4">{post.category}</Badge>
      <h1 className="text-3xl md:text-4xl font-bold">{post.title}</h1>
      <div className="flex items-center gap-4 mt-4 text-sm text-muted-foreground">
        <span>{post.author.name}</span>
        <span>·</span>
        <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{t.blog.readTime.replace("{{minutes}}", String(post.read_time))}</span>
        <span>·</span>
        <span>{formatDate(post.published_at, locale as Locale)}</span>
      </div>
      <div className="prose dark:prose-invert max-w-none mt-8">
        <p className="text-lg text-muted-foreground leading-relaxed">{post.excerpt}</p>
        <p className="mt-4 leading-relaxed">{post.content}</p>
      </div>
    </article>
  );
}
