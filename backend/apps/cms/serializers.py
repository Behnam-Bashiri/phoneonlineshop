from rest_framework import serializers

from apps.cms.models import (
    Banner,
    CustomerReview,
    FAQ,
    InstagramPost,
    LandingPage,
    LandingSection,
    Menu,
    MenuItem,
    NewsletterSubscriber,
    Page,
    Partner,
    SiteSettings,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "site_name",
            "site_name_fa",
            "logo",
            "logo_dark",
            "favicon",
            "phone",
            "email",
            "address",
            "address_fa",
            "social_instagram",
            "social_twitter",
            "social_telegram",
            "tax_rate",
            "currency",
            "currency_symbol",
            "free_shipping_threshold",
            "maintenance_mode",
            "default_meta_title",
            "default_meta_description",
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "id",
            "title",
            "title_fa",
            "slug",
            "content",
            "content_fa",
            "meta_title",
            "meta_description",
            "sort_order",
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "title",
            "title_fa",
            "url",
            "page",
            "category",
            "sort_order",
            "open_in_new_tab",
            "children",
        ]

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return MenuItemSerializer(children, many=True, context=self.context).data


class MenuSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "location", "items"]

    def get_items(self, obj):
        items = obj.items.filter(is_active=True, parent__isnull=True)
        return MenuItemSerializer(items, many=True, context=self.context).data


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "title",
            "title_fa",
            "subtitle",
            "image",
            "image_mobile",
            "link_url",
            "button_text",
            "location",
            "sort_order",
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "question_fa", "answer", "answer_fa", "category", "sort_order"]


class NewsletterSubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name", "logo", "website", "sort_order"]


class InstagramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = ["id", "image", "caption", "link_url", "sort_order"]


class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = [
            "id",
            "author_name",
            "content",
            "content_fa",
            "rating",
            "avatar",
            "is_featured",
            "sort_order",
        ]


class LandingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingSection
        fields = ["id", "section_type", "title", "content", "sort_order"]


class LandingPageSerializer(serializers.ModelSerializer):
    sections = LandingSectionSerializer(many=True, read_only=True)

    class Meta:
        model = LandingPage
        fields = ["id", "title", "slug", "meta_title", "meta_description", "sections"]


class HomePageSerializer(serializers.Serializer):
    banners = BannerSerializer(many=True)
    featured_products = serializers.ListField()
    special_offers = serializers.ListField()
    customer_reviews = CustomerReviewSerializer(many=True)
    partners = PartnerSerializer(many=True)
    instagram_posts = InstagramPostSerializer(many=True)
    site_settings = SiteSettingsSerializer()
