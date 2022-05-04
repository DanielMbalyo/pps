from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )

from src.account.api.serializers import UserDetailSerializer
from src.comment.api.serializers import CommentSerializer
from src.comment.models import Comment

from src.product.models import Product

product_detail_url = HyperlinkedIdentityField(
        view_name='product_api:detail',
        lookup_field='slug'
        )

class ProductCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'featured',
            'active',
            'is_digital',
        ]

class ProductDetailSerializer(ModelSerializer):
    url = product_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'description',
            'price',
            'featured',
            'active',
            'is_digital',
            'image',
            'comments',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

class ProductListSerializer(ModelSerializer):
    url = product_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            'url',
            'user',
            'title',
            'description',
            'price',
            'featured',
            'active',
            'is_digital',
        ]
