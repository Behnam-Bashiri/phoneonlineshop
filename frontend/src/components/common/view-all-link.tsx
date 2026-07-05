"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ViewAllLinkProps {
  href: string;
  label: string;
  className?: string;
}

export function ViewAllLink({ href, label, className }: ViewAllLinkProps) {
  return (
    <Button variant="ghost" asChild className={cn("group", className)}>
      <Link href={href}>
        {label}
        <ArrowRight className="ml-1 h-4 w-4 transition-transform group-hover:translate-x-1" />
      </Link>
    </Button>
  );
}
