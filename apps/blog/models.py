import datetime
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from filer.fields.image import FilerImageField
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
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    intro_picture = FilerImageField(related_name='blog_intro', on_delete=models.PROTECT)
    intro_picture_text = models.CharField(max_length=50, null=True, blank=True)
    picture_header = FilerImageField(related_name='blog_header', on_delete=models.PROTECT)
    picture_header_text = models.CharField(max_length=50, null=True, blank=True)
    picture_content = FilerImageField(related_name='blog_content', on_delete=models.PROTECT)
    picture_content_text = models.CharField(max_length=50, null=True, blank=True)
    intro = HTMLField()
    content = HTMLField()
    content2 = HTMLField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:slug', kwargs={'slug': self.slug})
