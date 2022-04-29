from django.contrib.postgres.fields import ArrayField, CICharField
import datetime

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from uuid import uuid4
from tinymce.models import HTMLField


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    intro = HTMLField()
    content = HTMLField()
    content2 = HTMLField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    tags = models.CharField(max_length=200)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    picture = models.ImageField(upload_to='blog')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:slug', kwargs={'slug': self.slug})

    @property
    def post_tags_list(self):
        tag_to_list = list()
        if "," in self.tags:
            tag_to_list = [x.strip() for x in self.tags.split(',')]
        else:
            tag_to_list.append(self.tags)
        return tag_to_list

    @staticmethod
    def blog_tags_list():
        def clean_tag(uncleaned_tag):
            cleaned_tag = str(uncleaned_tag)
            cleaned_tag = cleaned_tag.lower()
            cleaned_tag = cleaned_tag.strip()
            return cleaned_tag

        tag_to_set = set()
        posts_tag = Post.objects.values_list('tags')
        for post_tag in posts_tag:
            for tag in post_tag[0].split(','):
                if tag:
                    tag = clean_tag(tag)
                    tag_to_set.add(tag)
        return tag_to_set
