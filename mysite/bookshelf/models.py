from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_currentuser.middleware import get_current_user


class Author(models.Model):
    name = models.CharField(verbose_name='name', max_length=250)
    description = models.TextField(verbose_name='description')
    picture = models.ImageField(upload_to='author_pictures', blank=True)
    slug = models.SlugField(verbose_name='url', max_length=250, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse(viewname='author_detail', kwargs={'author_slug': self.slug})


class Book(models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    description = models.TextField(verbose_name='description')
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to='book_pictures', blank=True)
    slug = models.SlugField(verbose_name='url', max_length=250, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return reverse(viewname='book_detail', kwargs={'book_slug': self.slug})


class Comment(models.Model):
    name = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(verbose_name='text')
    date = models.DateTimeField(verbose_name='date', default=timezone.now)

    def __str__(self) -> str:
        return self.text

    def get_absolute_url(self) -> str:
        return reverse(viewname='book_detail', kwargs={'book_slug': self.book})

    def save(self, *args, **kwargs) -> None:
        if not self.name:
            user = get_current_user()
            self.name = User.objects.get(username=user)
        return super().save(*args, **kwargs)
