"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { Locale } from "@/lib/i18n";

interface ViewAllLinkProps {
  href: string;
  label: string;
  locale?: Locale;
  className?: string;
}

export function ViewAllLink({ href, label, locale, className }: ViewAllLinkProps) {
  return (
    <Button variant="ghost" asChild className={cn("group", className)}>
      <Link href={href}>
        {label}
        <ArrowRight
          className={cn(
            "ms-1 h-4 w-4 transition-transform group-hover:translate-x-1",
            locale === "fa" && "rotate-180 group-hover:-translate-x-1 group-hover:translate-x-0"
          )}
        />
      </Link>
    </Button>
  );
}
