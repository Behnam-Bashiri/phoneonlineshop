import Link from "next/link";
import { Smartphone, Facebook, Twitter, Instagram, Youtube } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import type { Locale } from "@/lib/i18n";
import { getTranslation } from "@/lib/translations";

interface FooterProps {
  locale: Locale;
}

export function Footer({ locale }: FooterProps) {
  const t = getTranslation(locale);
  const year = new Date().getFullYear();

  const quickLinks = [
    { href: `/${locale}/products`, label: t.common.products },
    { href: `/${locale}/blog`, label: t.common.blog },
    { href: `/${locale}/contact`, label: t.common.contact },
    { href: `/${locale}/pages/about`, label: t.footer.about },
  ];

  const serviceLinks = [
    { href: `/${locale}/pages/shipping`, label: "Shipping Info" },
    { href: `/${locale}/pages/returns`, label: "Returns" },
    { href: `/${locale}/pages/faq`, label: t.home.faq },
    { href: `/${locale}/account/tickets`, label: "Support" },
  ];

  const socialLinks = [
    { icon: Facebook, href: "#", label: "Facebook" },
    { icon: Twitter, href: "#", label: "Twitter" },
    { icon: Instagram, href: "#", label: "Instagram" },
    { icon: Youtube, href: "#", label: "Youtube" },
  ];

  return (
    <footer className="border-t bg-muted/30">
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <Link href={`/${locale}`} className="flex items-center gap-2 font-bold text-xl mb-4">
              <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                <Smartphone className="h-4 w-4 text-white" />
              </div>
              <span className="gradient-text">PhonyShop</span>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {t.footer.aboutDesc}
            </p>
            <div className="flex gap-3 mt-4">
              {socialLinks.map(({ icon: Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  className="h-9 w-9 rounded-full glass flex items-center justify-center hover:bg-accent transition-colors"
                >
                  <Icon className="h-4 w-4" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-4">{t.footer.quickLinks}</h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">{t.footer.customerService}</h3>
            <ul className="space-y-2">
              {serviceLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">{t.contact.info.email}</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>{t.contact.info.address}</li>
              <li>{t.contact.info.phone}</li>
              <li>{t.contact.info.email}</li>
              <li>{t.contact.info.hours}</li>
            </ul>
          </div>
        </div>

        <Separator className="my-8" />

        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
          <p>{t.footer.copyright.replace("{{year}}", String(year))}</p>
          <div className="flex gap-4">
            <Link href={`/${locale}/pages/privacy`} className="hover:text-foreground transition-colors">
              {t.footer.privacy}
            </Link>
            <Link href={`/${locale}/pages/terms`} className="hover:text-foreground transition-colors">
              {t.footer.terms}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
