from rest_framework import serializers
from .models import Blog, CustomUser
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "first_name", "last_name", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']          # ← added
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']

        user = get_user_model()
        new_user = user.objects.create_user(
            username=username,
            email=email,                         # ← added
            first_name=first_name,
            last_name=last_name,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user


# Renamed from VerySimpleUserSerializer to match views.py import
class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "profile_picture"]


class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True)  # ← updated name
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'author', 'category', 'content',
                  'featured_image', 'published_date', 'created_at', 'updated_at', 'is_draft']


class UserInfoSerializer(serializers.ModelSerializer):
    blog_posts = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "job_title",
                  "bio", "profile_picture", "facebook", "twitter",
                  "instagram", "linkedin", "blog_posts"]

    def get_blog_posts(self, user):
        blogs = user.blog_posts.all()[:9]
        serializer = BlogSerializer(blogs, many=True)
        return serializer.data


# Added — was missing but imported in views.py
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "job_title", "bio",
                  "profile_picture", "facebook", "twitter", "instagram", "linkedin"]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'job_title': {'required': False},
            'bio': {'required': False},
            'profile_picture': {'required': False},
            'facebook': {'required': False},
            'twitter': {'required': False},
            'instagram': {'required': False},
            'linkedin': {'required': False},
        }