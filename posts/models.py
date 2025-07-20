from django.db import models
from accounts.models import MyUser
from core.utls import generate_unique_slug_by_content

class Post(models.Model):
    slug = models.SlugField(unique=True, blank=True, editable=False)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    img = models.ImageField(null=True, blank=True, upload_to='posts/%Y-%m-%d')
    updated_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug_by_content(self.content)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.author.username

