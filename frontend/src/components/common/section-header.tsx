import { cn } from "@/lib/utils";

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  className?: string;
  align?: "left" | "center";
}

export function SectionHeader({
  title,
  subtitle,
  className,
  align = "left",
}: SectionHeaderProps) {
  return (
    <div
      className={cn(
        "mb-8 md:mb-12",
        align === "center" && "text-center",
        className
      )}
    >
      <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold tracking-tight">
        {title}
      </h2>
      {subtitle && (
        <p className="mt-2 text-muted-foreground text-sm md:text-base max-w-2xl mx-auto">
          {subtitle}
        </p>
      )}
    </div>
  );
}
