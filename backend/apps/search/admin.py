from django.contrib import admin

from apps.search.models import PopularSearch, SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ["query", "user", "results_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["query", "user__email"]


@admin.register(PopularSearch)
class PopularSearchAdmin(admin.ModelAdmin):
    list_display = ["query", "search_count", "is_featured"]
    list_filter = ["is_featured"]
    search_fields = ["query"]
