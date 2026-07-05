from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.blog.models import BlogCategory, BlogComment, BlogPost


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "name_fa", "slug", "description", "image"]


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "title_fa",
            "slug",
            "author",
            "category",
            "excerpt",
            "featured_image",
            "published_at",
            "reading_time_minutes",
            "view_count",
            "tags",
        ]

    def get_tags(self, obj):
        return list(obj.tags.names())


class BlogPostDetailSerializer(BlogPostListSerializer):
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            "content",
            "content_fa",
            "meta_title",
            "meta_description",
            "created_at",
        ]


class BlogCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        fields = ["id", "post", "user", "parent", "content", "is_approved", "replies", "created_at"]
        read_only_fields = ["id", "user", "is_approved", "created_at"]

    def get_replies(self, obj):
        if obj.parent_id:
            return []
        replies = obj.replies.filter(is_approved=True)
        return BlogCommentSerializer(replies, many=True, context=self.context).data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
