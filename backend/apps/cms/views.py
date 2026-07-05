from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.catalog.models import Product
from apps.catalog.serializers import ProductListSerializer
from apps.cms.models import (
    Banner,
    CustomerReview,
    FAQ,
    InstagramPost,
    LandingPage,
    Menu,
    NewsletterSubscriber,
    Page,
    Partner,
    SiteSettings,
)
from apps.cms.serializers import (
    BannerSerializer,
    CustomerReviewSerializer,
    FAQSerializer,
    HomePageSerializer,
    InstagramPostSerializer,
    LandingPageSerializer,
    MenuSerializer,
    NewsletterSubscribeSerializer,
    PageSerializer,
    PartnerSerializer,
    SiteSettingsSerializer,
)
from apps.promotions.models import SpecialOffer
from apps.promotions.serializers import SpecialOfferSerializer
from core.utils.pagination import StandardResultsSetPagination


class SiteSettingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            return Response({"detail": "Site settings not configured."}, status=status.HTTP_404_NOT_FOUND)
        return Response(SiteSettingsSerializer(settings, context={"request": request}).data)


class HomePageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()
        banners = Banner.objects.filter(is_active=True).filter(
            Q(starts_at__isnull=True) | Q(starts_at__lte=now),
            Q(ends_at__isnull=True) | Q(ends_at__gte=now),
        )[:10]

        featured_products = Product.objects.filter(
            is_active=True, is_deleted=False, is_featured=True
        ).select_related("brand", "category")[:12]

        special_offers = SpecialOffer.objects.filter(is_active=True)[:6]
        customer_reviews = CustomerReview.objects.filter(is_active=True, is_featured=True)[:10]
        partners = Partner.objects.filter(is_active=True)[:20]
        instagram_posts = InstagramPost.objects.filter(is_active=True)[:12]
        site_settings = SiteSettings.objects.first()

        data = {
            "banners": BannerSerializer(banners, many=True, context={"request": request}).data,
            "featured_products": ProductListSerializer(
                featured_products, many=True, context={"request": request}
            ).data,
            "special_offers": SpecialOfferSerializer(special_offers, many=True).data,
            "customer_reviews": CustomerReviewSerializer(customer_reviews, many=True).data,
            "partners": PartnerSerializer(partners, many=True).data,
            "instagram_posts": InstagramPostSerializer(instagram_posts, many=True).data,
            "site_settings": SiteSettingsSerializer(site_settings).data if site_settings else None,
        }
        return Response(data)


class PageViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.filter(is_published=True)
    serializer_class = PageSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"
    search_fields = ["title", "title_fa"]


class MenuViewSet(ReadOnlyModelViewSet):
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["location"]


class BannerViewSet(ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["location"]


class FAQViewSet(ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["category"]
    search_fields = ["question", "question_fa", "answer"]


class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewsletterSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=serializer.validated_data["email"],
            defaults={"is_active": True},
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active"])
        return Response(
            {"detail": "Successfully subscribed." if created else "Already subscribed."},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class PartnerViewSet(ReadOnlyModelViewSet):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    pagination_class = StandardResultsSetPagination


class InstagramPostViewSet(ReadOnlyModelViewSet):
    queryset = InstagramPost.objects.filter(is_active=True)
    serializer_class = InstagramPostSerializer
    pagination_class = StandardResultsSetPagination


class CustomerReviewViewSet(ReadOnlyModelViewSet):
    queryset = CustomerReview.objects.filter(is_active=True)
    serializer_class = CustomerReviewSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["is_featured"]


class LandingPageViewSet(ReadOnlyModelViewSet):
    queryset = LandingPage.objects.filter(is_published=True).prefetch_related("sections")
    serializer_class = LandingPageSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"
