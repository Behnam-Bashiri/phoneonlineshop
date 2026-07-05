import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-geist-sans",
});

export const metadata: Metadata = {
  title: {
    default: "PhonyShop - Premium Phones & Accessories",
    template: "%s | PhonyShop",
  },
  description:
    "Discover the latest smartphones from top brands at unbeatable prices. Premium phones, unmatched experience.",
  keywords: ["phones", "smartphones", "accessories", "mobile", "shop"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
