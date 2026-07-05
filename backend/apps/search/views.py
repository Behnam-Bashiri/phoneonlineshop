from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.catalog.serializers import ProductListSerializer
from apps.search.models import PopularSearch, SearchHistory
from apps.search.serializers import PopularSearchSerializer, SearchHistorySerializer
from apps.search.services import SearchService
from core.utils.pagination import StandardResultsSetPagination


class InstantSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if len(query) < 2:
            return Response({"query": query, "count": 0, "products": [], "suggestions": []})

        products = SearchService.search(query)
        suggestions = SearchService.get_suggestions(query)

        session_key = request.session.session_key or ""
        if not request.session.session_key:
            request.session.create()
            session_key = request.session.session_key

        user = request.user if request.user.is_authenticated else None
        SearchService.record_search(query, user=user, session_key=session_key, results_count=products.count())

        return Response({
            "query": query,
            "count": products.count(),
            "products": ProductListSerializer(products, many=True, context={"request": request}).data,
            "suggestions": suggestions,
        })


class SuggestionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        suggestions = SearchService.get_suggestions(query)
        return Response({"suggestions": suggestions})


class SearchHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)


class PopularSearchViewSet(ReadOnlyModelViewSet):
    queryset = PopularSearch.objects.all()
    serializer_class = PopularSearchSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return PopularSearch.objects.all().order_by("-search_count")
