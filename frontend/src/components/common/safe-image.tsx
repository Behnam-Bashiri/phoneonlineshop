"use client";

import Image from "next/image";
import { useState } from "react";
import { Smartphone } from "lucide-react";
import { cn } from "@/lib/utils";

interface SafeImageProps {
  src: string;
  alt: string;
  fill?: boolean;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
  sizes?: string;
}

export function SafeImage({
  src,
  alt,
  fill,
  width,
  height,
  className,
  priority,
  sizes,
}: SafeImageProps) {
  const [error, setError] = useState(false);

  if (error || !src) {
    return (
      <div
        className={cn(
          "flex items-center justify-center bg-gradient-to-br from-slate-200 to-slate-300 dark:from-slate-800 dark:to-slate-900",
          fill && "absolute inset-0",
          className
        )}
        style={!fill && width && height ? { width, height } : undefined}
      >
        <Smartphone className="h-12 w-12 text-muted-foreground/50" />
      </div>
    );
  }

  if (fill) {
    return (
      <Image
        src={src}
        alt={alt}
        fill
        className={className}
        priority={priority}
        sizes={sizes ?? "(max-width: 768px) 100vw, 50vw"}
        onError={() => setError(true)}
      />
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      width={width ?? 120}
      height={height ?? 120}
      className={className}
      priority={priority}
      onError={() => setError(true)}
    />
  );
}
