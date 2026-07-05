import { AccountSidebar } from "@/components/account/account-sidebar";
import type { Locale } from "@/lib/i18n";

export default async function AccountLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="grid lg:grid-cols-4 gap-8">
        <aside className="lg:col-span-1">
          <div className="glass-card p-4 sticky top-24">
            <AccountSidebar locale={locale as Locale} />
          </div>
        </aside>
        <div className="lg:col-span-3">{children}</div>
      </div>
    </div>
  );
}
