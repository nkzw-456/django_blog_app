from django.db import models
from django.utils.crypto import get_random_string


def create_id():
    return get_random_string(22)


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    name_eng = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def post_count(self):
        num = Blog.objects.filter(category = self).count()
        return num

    def __str__(self):
        return self.name



class Blog(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=22,
    editable=False)
    title = models.CharField(max_length=50)
    images = models.ImageField(upload_to='images/', blank=True)
    body = models.TextField(max_length=1000)
    author = models.CharField(max_length=20)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=500, default='')
    name = models.CharField(max_length=20, default='')
    created_at = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]
