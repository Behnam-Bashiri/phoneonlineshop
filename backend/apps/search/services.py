from django.db.models import Q

from apps.catalog.models import Brand, Category, Product
from apps.search.models import PopularSearch, SearchHistory


class SearchService:
    @staticmethod
    def search(query, limit=20):
        if not query or len(query.strip()) < 2:
            return Product.objects.none()

        q = query.strip()
        products = Product.objects.filter(
            is_active=True,
            is_deleted=False,
        ).filter(
            Q(name__icontains=q)
            | Q(name_fa__icontains=q)
            | Q(sku__icontains=q)
            | Q(description__icontains=q)
            | Q(brand__name__icontains=q)
            | Q(category__name__icontains=q)
        ).select_related("brand", "category").distinct()[:limit]

        return products

    @staticmethod
    def get_suggestions(query, limit=10):
        if not query or len(query.strip()) < 2:
            return []

        q = query.strip()
        suggestions = []

        products = Product.objects.filter(
            is_active=True,
            is_deleted=False,
            name__icontains=q,
        ).values_list("name", flat=True)[:limit]
        suggestions.extend(products)

        brands = Brand.objects.filter(is_active=True, name__icontains=q).values_list("name", flat=True)[:5]
        suggestions.extend(brands)

        categories = Category.objects.filter(is_active=True, name__icontains=q).values_list("name", flat=True)[:5]
        suggestions.extend(categories)

        popular = PopularSearch.objects.filter(query__icontains=q).values_list("query", flat=True)[:5]
        suggestions.extend(popular)

        seen = set()
        unique = []
        for item in suggestions:
            if item.lower() not in seen:
                seen.add(item.lower())
                unique.append(item)
        return unique[:limit]

    @staticmethod
    def record_search(query, user=None, session_key="", results_count=0):
        SearchHistory.objects.create(
            user=user if user and user.is_authenticated else None,
            query=query,
            results_count=results_count,
            session_key=session_key,
        )
        popular, created = PopularSearch.objects.get_or_create(query=query.lower())
        if not created:
            popular.search_count += 1
            popular.save(update_fields=["search_count"])
