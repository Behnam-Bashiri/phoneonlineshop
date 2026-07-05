from rest_framework import serializers

from apps.catalog.models import (
    Brand,
    Category,
    Color,
    PriceAlert,
    Product,
    ProductComparison,
    ProductImage,
    ProductSpecification,
    ProductVariant,
    ProductVideo,
    RAMOption,
    RecentlyViewed,
    StorageOption,
    Wishlist,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "name_fa",
            "slug",
            "logo",
            "description",
            "website",
            "is_active",
            "sort_order",
        ]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "name_fa",
            "slug",
            "parent",
            "image",
            "icon",
            "description",
            "is_active",
            "sort_order",
            "children",
        ]

    def get_children(self, obj):
        if self.context.get("include_children"):
            children = obj.get_children().filter(is_active=True)
            return CategorySerializer(children, many=True, context=self.context).data
        return []


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["id", "name", "name_fa", "hex_code", "is_active"]


class StorageOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageOption
        fields = ["id", "capacity", "capacity_gb", "is_active"]


class RAMOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMOption
        fields = ["id", "capacity", "capacity_gb", "is_active"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "sort_order", "is_primary", "variant"]


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ["id", "title", "video_url", "video_file", "thumbnail", "sort_order"]


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            "id",
            "group_name",
            "group_name_fa",
            "name",
            "name_fa",
            "value",
            "value_fa",
            "sort_order",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    storage = StorageOptionSerializer(read_only=True)
    ram = RAMOptionSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source="color", write_only=True, required=False, allow_null=True
    )
    storage_id = serializers.PrimaryKeyRelatedField(
        queryset=StorageOption.objects.all(), source="storage", write_only=True, required=False, allow_null=True
    )
    ram_id = serializers.PrimaryKeyRelatedField(
        queryset=RAMOption.objects.all(), source="ram", write_only=True, required=False, allow_null=True
    )
    available_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "color",
            "storage",
            "ram",
            "color_id",
            "storage_id",
            "ram_id",
            "price",
            "compare_price",
            "stock_quantity",
            "reserved_quantity",
            "available_stock",
            "is_active",
            "is_default",
            "image",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "name_fa",
            "slug",
            "sku",
            "brand",
            "category",
            "short_description",
            "base_price",
            "compare_price",
            "is_active",
            "is_featured",
            "is_new_arrival",
            "is_best_seller",
            "average_rating",
            "review_count",
            "primary_image",
            "tags",
            "created_at",
        ]

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image:
            request = self.context.get("request")
            url = image.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_tags(self, obj):
        return list(obj.tags.names())


class ProductDetailSerializer(ProductListSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    advantages = serializers.JSONField()
    disadvantages = serializers.JSONField()
    features = serializers.JSONField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            "description",
            "description_fa",
            "barcode",
            "has_360_view",
            "warranty_months",
            "weight_grams",
            "view_count",
            "sold_count",
            "meta_title",
            "meta_description",
            "og_image",
            "advantages",
            "disadvantages",
            "features",
            "variants",
            "images",
            "videos",
            "specifications",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True, is_deleted=False),
        source="product",
        write_only=True,
    )
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.filter(is_active=True),
        source="variant",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_id", "variant", "variant_id", "created_at"]
        read_only_fields = ["id", "variant", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class RecentlyViewedSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = RecentlyViewed
        fields = ["id", "product", "viewed_at"]


class ProductComparisonSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = ProductComparison
        fields = ["id", "products", "product_ids", "created_at"]
        read_only_fields = ["id", "created_at"]


class PriceAlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = PriceAlert
        fields = [
            "id",
            "product",
            "variant",
            "product_name",
            "target_price",
            "is_active",
            "notified",
            "created_at",
        ]
        read_only_fields = ["id", "notified", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
