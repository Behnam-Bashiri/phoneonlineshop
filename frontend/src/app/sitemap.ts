import type { MetadataRoute } from "next";

const locales = ["en", "fa"];

const staticPages = [
  "",
  "/products",
  "/blog",
  "/contact",
  "/search",
  "/compare",
  "/wishlist",
  "/cart",
  "/auth/login",
  "/auth/register",
];

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://phonyshop.com";

  const entries: MetadataRoute.Sitemap = [];

  for (const locale of locales) {
    for (const page of staticPages) {
      entries.push({
        url: `${baseUrl}/${locale}${page}`,
        lastModified: new Date(),
        changeFrequency: page === "" ? "daily" : "weekly",
        priority: page === "" ? 1 : 0.8,
        alternates: {
          languages: {
            en: `${baseUrl}/en${page}`,
            fa: `${baseUrl}/fa${page}`,
          },
        },
      });
    }
  }

  return entries;
}
