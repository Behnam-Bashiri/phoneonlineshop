from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.cms.views import (
    BannerViewSet,
    CustomerReviewViewSet,
    FAQViewSet,
    HomePageView,
    InstagramPostViewSet,
    LandingPageViewSet,
    MenuViewSet,
    NewsletterSubscribeView,
    PageViewSet,
    PartnerViewSet,
    SiteSettingsView,
)

router = DefaultRouter()
router.register("pages", PageViewSet, basename="page")
router.register("menus", MenuViewSet, basename="menu")
router.register("banners", BannerViewSet, basename="banner")
router.register("faq", FAQViewSet, basename="faq")
router.register("partners", PartnerViewSet, basename="partner")
router.register("instagram", InstagramPostViewSet, basename="instagram")
router.register("customer-reviews", CustomerReviewViewSet, basename="customer-review")
router.register("landing-pages", LandingPageViewSet, basename="landing-page")

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("newsletter/subscribe/", NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
    path("", include(router.urls)),
]
