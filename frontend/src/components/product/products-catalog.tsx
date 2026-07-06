"use client";

import { useState, useCallback, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import { Grid3X3, List, SlidersHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { ProductCard } from "@/components/product/product-card";
import { useInfiniteScroll } from "@/hooks/use-infinite-scroll";
import { getMockProducts, getMockCategories, getMockBrands } from "@/lib/mock-data";
import { getTranslation, translate } from "@/lib/translations";
import { formatPrice } from "@/lib/utils";
import type { Locale } from "@/lib/i18n";

const PAGE_SIZE = 6;

interface ProductsCatalogProps {
  locale: Locale;
}

export function ProductsCatalog({ locale }: ProductsCatalogProps) {
  const searchParams = useSearchParams();
  const t = getTranslation(locale);
  const mockProducts = getMockProducts(locale);
  const mockCategories = getMockCategories(locale);
  const mockBrands = getMockBrands(locale);

  const [view, setView] = useState<"grid" | "list">("grid");
  const [sort, setSort] = useState(searchParams.get("sort") || "newest");
  const [priceRange, setPriceRange] = useState([0, 1500]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedBrands, setSelectedBrands] = useState<string[]>([]);
  const [page, setPage] = useState(1);

  const filteredProducts = useMemo(() => {
    let products = [...mockProducts];

    const category = searchParams.get("category");
    const brand = searchParams.get("brand");
    if (category) products = products.filter((p) => p.category.slug === category);
    if (brand) products = products.filter((p) => p.brand?.slug === brand);
    if (selectedCategories.length)
      products = products.filter((p) => selectedCategories.includes(p.category.slug));
    if (selectedBrands.length)
      products = products.filter((p) => p.brand && selectedBrands.includes(p.brand.slug));

    products = products.filter(
      (p) => p.price >= priceRange[0] && p.price <= priceRange[1]
    );

    switch (sort) {
      case "priceAsc":
        products.sort((a, b) => a.price - b.price);
        break;
      case "priceDesc":
        products.sort((a, b) => b.price - a.price);
        break;
      case "popular":
        products.sort((a, b) => b.review_count - a.review_count);
        break;
      case "rating":
        products.sort((a, b) => b.rating - a.rating);
        break;
      default:
        products.sort(
          (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
    }

    return products;
  }, [sort, priceRange, selectedCategories, selectedBrands, searchParams]);

  const displayedProducts = filteredProducts.slice(0, page * PAGE_SIZE);
  const hasMore = displayedProducts.length < filteredProducts.length;

  const loadMore = useCallback(() => {
    if (hasMore) setPage((p) => p + 1);
  }, [hasMore]);

  const loadMoreRef = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    isLoading: false,
  });

  const FilterContent = () => (
    <div className="space-y-6">
      <div>
        <Label className="mb-3 block font-semibold">{t.products.filters}</Label>
        <div className="space-y-3">
          <Label className="text-sm text-muted-foreground">{t.filters.priceRange}</Label>
          <Slider
            value={priceRange}
            onValueChange={setPriceRange}
            max={1500}
            step={50}
            className="mt-2"
          />
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>{formatPrice(priceRange[0], locale)}</span>
            <span>{formatPrice(priceRange[1], locale)}</span>
          </div>
        </div>
      </div>

      <div>
        <Label className="mb-3 block font-semibold">{t.filters.categories}</Label>
        <div className="space-y-2">
          {mockCategories.map((cat) => (
            <div key={cat.id} className="flex items-center gap-2">
              <Checkbox
                id={`cat-${cat.slug}`}
                checked={selectedCategories.includes(cat.slug)}
                onCheckedChange={(checked) => {
                  setSelectedCategories((prev) =>
                    checked
                      ? [...prev, cat.slug]
                      : prev.filter((s) => s !== cat.slug)
                  );
                  setPage(1);
                }}
              />
              <label htmlFor={`cat-${cat.slug}`} className="text-sm cursor-pointer">
                {cat.name}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <Label className="mb-3 block font-semibold">{t.filters.brands}</Label>
        <div className="space-y-2">
          {mockBrands.map((brand) => (
            <div key={brand.id} className="flex items-center gap-2">
              <Checkbox
                id={`brand-${brand.slug}`}
                checked={selectedBrands.includes(brand.slug)}
                onCheckedChange={(checked) => {
                  setSelectedBrands((prev) =>
                    checked
                      ? [...prev, brand.slug]
                      : prev.filter((s) => s !== brand.slug)
                  );
                  setPage(1);
                }}
              />
              <label htmlFor={`brand-${brand.slug}`} className="text-sm cursor-pointer">
                {brand.name}
              </label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">{t.products.title}</h1>
          <p className="text-muted-foreground mt-1">
            {translate(locale, "products.showing", { count: filteredProducts.length })}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Select value={sort} onValueChange={(v) => { setSort(v); setPage(1); }}>
            <SelectTrigger className="w-[180px] hidden sm:flex">
              <SelectValue placeholder={t.products.sort} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="newest">{t.products.sortOptions.newest}</SelectItem>
              <SelectItem value="priceAsc">{t.products.sortOptions.priceAsc}</SelectItem>
              <SelectItem value="priceDesc">{t.products.sortOptions.priceDesc}</SelectItem>
              <SelectItem value="popular">{t.products.sortOptions.popular}</SelectItem>
              <SelectItem value="rating">{t.products.sortOptions.rating}</SelectItem>
            </SelectContent>
          </Select>
          <div className="hidden sm:flex border rounded-xl overflow-hidden">
            <Button
              variant={view === "grid" ? "secondary" : "ghost"}
              size="icon"
              onClick={() => setView("grid")}
            >
              <Grid3X3 className="h-4 w-4" />
            </Button>
            <Button
              variant={view === "list" ? "secondary" : "ghost"}
              size="icon"
              onClick={() => setView("list")}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="lg:hidden">
                <SlidersHorizontal className="h-4 w-4" />
              </Button>
            </SheetTrigger>
            <SheetContent side={locale === "fa" ? "right" : "left"}>
              <SheetHeader>
                <SheetTitle>{t.products.filters}</SheetTitle>
              </SheetHeader>
              <div className="mt-6">
                <FilterContent />
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        <aside className="hidden lg:block">
          <div className="glass-card p-6 sticky top-24">
            <FilterContent />
          </div>
        </aside>

        <div className="lg:col-span-3">
          {displayedProducts.length === 0 ? (
            <div className="text-center py-16">
              <p className="text-muted-foreground">{t.products.noProducts}</p>
            </div>
          ) : (
            <div
              className={
                view === "grid"
                  ? "grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6"
                  : "space-y-4"
              }
            >
              {displayedProducts.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  locale={locale}
                  view={view}
                />
              ))}
            </div>
          )}
          {hasMore && <div ref={loadMoreRef} className="h-10 mt-8" />}
        </div>
      </div>
    </div>
  );
}
