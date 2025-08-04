from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

# --- Define the Category Model FIRST ---
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

# --- Now define BlogPost (which references Category) ---
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="A unique slug for the URL, e.g., 'my-awesome-blog-post'")
    content = RichTextUploadingField()
    excerpt = models.TextField(
        blank=True,
        null=True,
        help_text="A short summary or teaser of the blog post, usually plain text. Used for list views."
    )
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Whether the blog post is currently active/visible")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# --- Rest of your models should follow ---
# Event model
class Event(models.Model):
    title = models.CharField(max_length=200, help_text="Name of the event")
    slug = models.SlugField(max_length=200, unique=True, help_text="A unique slug for the URL, e.g., 'annual-dental-camp'")
    description = models.TextField(help_text="Detailed description of the event")
    event_date = models.DateTimeField(help_text="Date and time of the event")
    location = models.CharField(max_length=255, help_text="Venue or online link for the event")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text="Optional image for the event")
    is_active = models.BooleanField(default=True, help_text="Whether the event is currently active/visible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title

# ContactMessage model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the person sending the message")
    email = models.EmailField(help_text="Email address for reply")
    subject = models.CharField(max_length=200, blank=True, null=True, help_text="Subject of the message (optional)")
    message = models.TextField(help_text="The content of the message")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the message was sent")
    is_read = models.BooleanField(default=False, help_text="Mark if the message has been read by an admin")

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

# NewsletterSubscriber model
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, help_text="Email address of the subscriber")
    subscribed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the user subscribed")
    is_active = models.BooleanField(default=True, help_text="Whether the subscription is currently active")

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

# Resource model
class Resource(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the downloadable resource")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the resource")
    file = models.FileField(upload_to='resources/', help_text="The actual file for download (PDFs, documents, etc.)")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the resource was uploaded")
    is_public = models.BooleanField(default=True, help_text="Whether the resource is publicly available")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

# --- NEW: Volunteer Application Model ---
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

    def __str__(self):
        return f"Volunteer: {self.name} - {self.area_of_interest}"

    class Meta:
        verbose_name = "Volunteer Application"
        verbose_name_plural = "Volunteer Applications"
        ordering = ['-application_date']

# --- NEW: Partnership Inquiry Model ---
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

    def __str__(self):
        return f"Partnership: {self.organization_name} - {self.contact_person}"

    class Meta:
        verbose_name = "Partnership Inquiry"
        verbose_name_plural = "Partnership Inquiries"
        ordering = ['-inquiry_date']

# --- NEW: Team Member Model ---
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='team_members/', blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    twitter_url = models.URLField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order in which team members appear")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name']

# --- UPDATED: Gallery Item Model ---
class GalleryItem(models.Model):
    image = models.ImageField(upload_to='gallery_images/', blank=True, null=True)
    video = models.FileField(upload_to='gallery_videos/', blank=True, null=True, help_text="Optional: Upload a video file instead of an image.")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    # --- CHANGED: `category` is now a ForeignKey to the Category model ---
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # If a category is deleted, set this field to NULL
        null=True,                # Allow null values in the database
        blank=True,               # Allow the field to be blank in forms/admin
        related_name='gallery_items', # Allows reverse lookup: category.gallery_items.all()
        help_text="Assign a category (e.g., Program, Location) to this gallery item."
    )
    is_published = models.BooleanField(default=True)

    def __str__(self):
        # Include category name in string representation for clarity
        if self.category:
            return f"{self.title} ({self.category.name})"
        return self.title

    class Meta:
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
        ordering = ['-upload_date']