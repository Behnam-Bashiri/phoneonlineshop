from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class SearchHistory(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255, db_index=True)
    results_count = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "search_history"
        ordering = ["-created_at"]
        verbose_name_plural = "search histories"


class PopularSearch(TimeStampedModel):
    query = models.CharField(max_length=255, unique=True)
    search_count = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = "popular_searches"
        ordering = ["-search_count"]
