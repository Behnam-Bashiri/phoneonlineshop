import { Skeleton } from "@/components/ui/skeleton";

export function ProductCardSkeleton({ view = "grid" }: { view?: "grid" | "list" }) {
  if (view === "list") {
    return (
      <div className="flex gap-4 p-4 rounded-2xl border">
        <Skeleton className="w-48 h-48 rounded-xl shrink-0" />
        <div className="flex-1 space-y-3">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-6 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
          <div className="flex justify-between items-center pt-4">
            <Skeleton className="h-8 w-24" />
            <Skeleton className="h-9 w-28 rounded-xl" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border overflow-hidden">
      <Skeleton className="aspect-square w-full" />
      <div className="p-4 space-y-2">
        <Skeleton className="h-3 w-16" />
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-3 w-20" />
        <div className="flex justify-between items-center pt-2">
          <Skeleton className="h-6 w-20" />
          <Skeleton className="h-8 w-8 rounded-full" />
        </div>
      </div>
    </div>
  );
}

export function ProductGridSkeleton({ count = 8 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <ProductCardSkeleton key={i} />
      ))}
    </div>
  );
}
