# PleromaSpringsWebsite/p-backend/core_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# NEW: Import all your views
from .views import (
    BlogPostViewSet, EventViewSet, ResourceViewSet,
    ContactMessageCreateView, NewsletterSubscriberCreateView,
    VolunteerApplicationCreateView, PartnershipInquiryCreateView, # New form views
    TeamMemberViewSet, GalleryItemViewSet, CategoryViewSet # New data views
)

# Create a router and register our viewsets with it.
# ViewSets handle multiple HTTP methods (GET, POST, PUT, DELETE) for a single resource.
# ReadOnlyModelViewSet provides list and retrieve actions.
router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet, basename='blogpost') # Register BlogPostViewSet
router.register(r'events', EventViewSet, basename='event') # Register EventViewSet
router.register(r'resources', ResourceViewSet, basename='resource') # Register ResourceViewSet
router.register(r'team-members', TeamMemberViewSet, basename='team-member') # NEW: Team Members API
router.register(r'gallery-items', GalleryItemViewSet, basename='gallery-item') # NEW: Gallery API
router.register(r'categories', CategoryViewSet, basename='category') # NEW: Categories API

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)), # Includes all URLs registered with the router

    # Specific API Endpoints for form submissions (using CreateAPIView)
    path('contact/', ContactMessageCreateView.as_view(), name='contact-message-create'),
    path('subscribe/', NewsletterSubscriberCreateView.as_view(), name='newsletter-subscribe'),
    path('volunteer/', VolunteerApplicationCreateView.as_view(), name='volunteer-application-create'), # NEW: Volunteer form API
    path('partner/', PartnershipInquiryCreateView.as_view(), name='partnership-inquiry-create'), # NEW: Partner form API
    # Add any other specific endpoints you need here
]