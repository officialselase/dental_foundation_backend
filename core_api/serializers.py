from rest_framework import serializers
from .models import (
    BlogPost, Event, ContactMessage, NewsletterSubscriber, Resource,
    VolunteerApplication, PartnershipInquiry, TeamMember, GalleryItem,
    Category
)

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

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content',
            'excerpt',
            'author', 'published_date', 'updated_date', 'image', 'is_active',
            'category',
            'category_id'
        ]
        read_only_fields = ['slug', 'published_date', 'updated_date', 'category']

# --- Event Serializer ---
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'event_date', 'location', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

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
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'file', 'uploaded_at', 'is_public']
        read_only_fields = ['uploaded_at']

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
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'profile_picture', 'linkedin_url', 'twitter_url', 'email', 'order', 'is_active']
        read_only_fields = ['id']

# --- UPDATED: GalleryItem Serializer ---
class GalleryItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    # --- ADDED: Nested CategorySerializer for reading category details ---
    category = CategorySerializer(read_only=True)
    # --- ADDED: category_id for writing/updating using the category's primary key ---
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category', # Maps this field to the 'category' ForeignKey
        write_only=True,   # Only used for writing (input), not for reading (output)
        required=False,    # Make it optional if a gallery item doesn't always need a category
        allow_null=True    # Allow null if the ForeignKey in models.py has null=True
    )

    class Meta:
        model = GalleryItem
        fields = ['id', 'image', 'video', 'title', 'description', 'upload_date', 'category', 'category_id', 'is_published'] # Added category_id
        read_only_fields = ['upload_date', 'category'] # category is read-only when shown as full object