from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# always remember that since these variables are directly in the class and not the init constructor they are class variables


class PublishedManager(models.Manager):
    """A PublishedManager manager model class to handle all published queries"""

    def get_queryset(self):
        return super().get_queryset().filter(status='published')
        # or return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    # the slug is a field intended to be used in URLs.
    # To build beautiful and awesome SEO-friendly URLs for the blog posts
    # The URLs are built using the unique_for_date parameter which build URLs using
    # their publish date and slug
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # models.CASCADE field shows that when referenced model(in this case User) is deleted, the related blog posts of the 
    # referenced User should also be deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # the negative prefix specifies a descending order
        # Posts published recently will appear first
        ordering = ('-publish',)  # have to bring the comma after this else a model.E014 error appears where 'ordering'
        # must be a tuple or a list even if you want to order by one field

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """It is a Django convention to add a get_absolute_url method to the model that returns the
        canonical URL(in this case the Post model)"""

        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    # managers of Post
    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager
    tags = TaggableManager() # tag manager


class Comment(models.Model):
    """A comment system in a many-to-one relationship with a single Post instance"""
    # related_name attribute allows the renaming of the attribute used for relation back to the related object
    # if using the DB API now, instead of Post.comment_set.all() to retrive objects,
    # it can be Post.comments.all
    # so by default if you don't set the related_name, Django will create a lowercase of the model with _set added
    # to name the manager of the related object like seen in Post.comment_set.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # this will be used to deactivate inappropriate comments
    active = models.BooleanField(default=True)


    class Meta:
        # always remember: class Meta makes you select which field to post your model by.
        # comments will be posted based on time of creation
        ordering = ('created',)


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'




    
    








# Create your models here

