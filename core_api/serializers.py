# core_api/serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import (
    BlogPost, Event, ContactMessage, NewsletterSubscriber, Resource,
    VolunteerApplication, PartnershipInquiry, TeamMember, GalleryItem,
    Category, ImpactStat, TransformationStory
)

def absolute_url_for_field(instance, field_name, request):
    """Helper: return absolute URL for an ImageField/FileField or None."""
    f = getattr(instance, field_name, None)
    if not f:
        return None
    try:
        url = f.url
    except ValueError:
        return None
    if request is None:
        # fallback to MEDIA_URL
        return settings.MEDIA_URL + str(f)
    return request.build_absolute_uri(url)

# --- Category Serializer ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

# --- BlogPost Serializer ---
class BlogPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author',
            'published_date', 'updated_date', 'image', 'image_url', 'is_active',
            'category', 'category_id'
        ]
        read_only_fields = ['slug', 'published_date', 'updated_date', 'category']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'image', request)


# --- Event Serializer ---
class EventSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'event_date', 'location', 'image', 'image_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'image', request)


# --- ContactMessage Serializer ---
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'submitted_at', 'is_read']
        read_only_fields = ['submitted_at', 'is_read']


# --- NewsletterSubscriber Serializer ---
class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at', 'is_active']
        read_only_fields = ['subscribed_at', 'is_active']


# --- Resource Serializer ---
class ResourceSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'file', 'file_url', 'uploaded_at', 'is_public']
        read_only_fields = ['uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'file', request)


# --- Volunteer Application Serializer ---
class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = ['id', 'name', 'email', 'phone', 'area_of_interest', 'message', 'application_date', 'status']
        read_only_fields = ['application_date', 'status']


# --- Partnership Inquiry Serializer ---
class PartnershipInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipInquiry
        fields = ['id', 'organization_name', 'contact_person', 'email', 'partnership_type', 'message', 'inquiry_date', 'status']
        read_only_fields = ['inquiry_date', 'status']


# --- TeamMember Serializer ---
class TeamMemberSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'profile_picture', 'profile_picture_url', 'linkedin_url', 'twitter_url', 'email', 'order', 'is_active']
        read_only_fields = ['id']

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'profile_picture', request)


# --- GalleryItem Serializer ---
class GalleryItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = GalleryItem
        fields = ['id', 'image', 'image_url', 'video', 'video_url', 'title', 'description', 'upload_date', 'category', 'category_id', 'is_published']
        read_only_fields = ['upload_date', 'category']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'image', request)

    def get_video_url(self, obj):
        request = self.context.get('request')
        return absolute_url_for_field(obj, 'video', request)


# --- ImpactStat Serializer ---
class ImpactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStat
        fields = '__all__'


# --- TransformationStory Serializer ---
class TransformationStorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TransformationStory
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        # if TransformationStory has an image field name other than 'image', change accordingly
        return absolute_url_for_field(obj, 'image', request)
