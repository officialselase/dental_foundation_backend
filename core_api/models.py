from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify


# --- Category Model ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --- BlogPost Model ---
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique slug for the URL")
    content = RichTextUploadingField()
    excerpt = models.TextField(blank=True, null=True, help_text="Short summary for list views.")
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# --- Event Model ---
class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title


# --- ContactMessage Model ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


# --- NewsletterSubscriber Model ---
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


# --- Resource Model ---
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


# --- Volunteer Application Model ---
class VolunteerApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    area_of_interest = models.CharField(max_length=100, choices=[
        ('Community Outreach', 'Community Outreach'),
        ('Education & Training', 'Education & Training'),
        ('Administrative Support', 'Administrative Support'),
        ('Fundraising', 'Fundraising'),
        ('Other', 'Other'),
    ])
    message = models.TextField(blank=True, null=True)
    application_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Contacted', 'Contacted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ])

    class Meta:
        verbose_name = "Volunteer Application"
        verbose_name_plural = "Volunteer Applications"
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.name} - {self.area_of_interest}"


# --- Partnership Inquiry Model ---
class PartnershipInquiry(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    partnership_type = models.CharField(max_length=100, choices=[
        ('Program Collaboration', 'Program Collaboration'),
        ('Funding/Sponsorship', 'Funding/Sponsorship'),
        ('Research', 'Research'),
        ('Advocacy', 'Advocacy'),
        ('Other', 'Other'),
    ])
    message = models.TextField(blank=True, null=True)
    inquiry_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='New', choices=[
        ('New', 'New'),
        ('Reviewed', 'Reviewed'),
        ('Contacted', 'Contacted'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
    ])

    class Meta:
        verbose_name = "Partnership Inquiry"
        verbose_name_plural = "Partnership Inquiries"
        ordering = ['-inquiry_date']

    def __str__(self):
        return f"{self.organization_name} - {self.contact_person}"


# --- Team Member Model ---
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='team_members/', blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    twitter_url = models.URLField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.role})"


# --- Gallery Item Model ---
class GalleryItem(models.Model):
    image = models.ImageField(upload_to='gallery_images/', blank=True, null=True)
    video = models.FileField(upload_to='gallery_videos/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} ({self.category.name})" if self.category else self.title


# --- NEW: ImpactStat Model ---
class ImpactStat(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)  # e.g. "10,000+", "85%"
    icon = models.ImageField(upload_to='impact_icons/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.value}"


# --- NEW: TransformationStory Model ---
class TransformationStory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    story = models.TextField()
    image = models.ImageField(upload_to='transformation_stories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Story by {self.name}"
