from rest_framework import serializers

from apps.catalog.serializers import ProductListSerializer
from apps.search.models import PopularSearch, SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["id", "query", "results_count", "created_at"]
        read_only_fields = fields


class PopularSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularSearch
        fields = ["id", "query", "search_count", "is_featured"]


class InstantSearchSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=255)


class SearchResultSerializer(serializers.Serializer):
    query = serializers.CharField()
    count = serializers.IntegerField()
    products = ProductListSerializer(many=True)
    suggestions = serializers.ListField(child=serializers.CharField())
