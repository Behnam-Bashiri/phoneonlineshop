import type { Metadata } from "next";
import type { Locale } from "@/lib/i18n";

const cmsPages: Record<string, { title: string; content: string }> = {
  about: {
    title: "About PhonyShop",
    content: "PhonyShop is your trusted destination for premium smartphones and accessories. Since 2020, we've been delivering the latest devices from top brands with unmatched customer service and competitive prices.",
  },
  privacy: {
    title: "Privacy Policy",
    content: "We respect your privacy and are committed to protecting your personal data. This policy explains how we collect, use, and safeguard your information when you use our services.",
  },
  terms: {
    title: "Terms of Service",
    content: "By using PhonyShop, you agree to these terms. Please read them carefully. These terms govern your use of our website, mobile applications, and services.",
  },
  shipping: {
    title: "Shipping Information",
    content: "We offer free standard shipping on orders over $50. Express shipping is available for an additional fee. International shipping is available to over 50 countries.",
  },
  returns: {
    title: "Returns & Refunds",
    content: "We offer a 30-day hassle-free return policy. Items must be in original condition with all accessories. Refunds are processed within 5-7 business days after we receive the return.",
  },
  faq: {
    title: "FAQ",
    content: "Find answers to commonly asked questions about orders, shipping, returns, products, and account management.",
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const page = cmsPages[slug];
  return { title: page?.title || "Page" };
}

export function generateStaticParams() {
  return Object.keys(cmsPages).map((slug) => ({ slug }));
}

export default async function CMSPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { slug } = await params;
  const page = cmsPages[slug];

  if (!page) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold">Page Not Found</h1>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 md:py-12 max-w-3xl">
      <h1 className="text-3xl font-bold mb-8">{page.title}</h1>
      <div className="glass-card p-6 md:p-8 prose dark:prose-invert max-w-none">
        <p className="text-muted-foreground leading-relaxed">{page.content}</p>
      </div>
    </div>
  );
}
