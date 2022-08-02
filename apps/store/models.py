from decimal import Decimal
from uuid import uuid4

from azbankgateways.models import Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from tinymce.models import HTMLField

from apps.account.models import UserProfile
from config.settings.base import LANGUAGES


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    status = models.CharField(max_length=50, choices=STATUS, default='Draft')
    code = models.CharField(max_length=11, blank=True, unique=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, allow_unicode=True)
    label_text = models.CharField(max_length=20)
    label_color = models.CharField(max_length=20)
    intro = models.TextField(max_length=1000)
    description = HTMLField()
    more_info = HTMLField()
    send_and_return = HTMLField()
    stock_inventory = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, default=Decimal('0.0'),
                                validators=(MinValueValidator(Decimal('0.0')),))
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    introduction_picture = FilerImageField(related_name='store_picture_introduction', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.code = f"sep-{self.id:07d}"
        super().save(*args, **kwargs)

    @property
    def absolute_url(self):
        return reverse('store:product-code-slug', kwargs={'slug': self.slug, 'pk': self.code})

    def get_absolute_url(self):
        return reverse('store:product-code-slug', kwargs={'slug': self.slug, 'pk': self.code})

    # def clean(self):
    # if self.has_variant is False and self.price is None:
    #     raise ValidationError(_('a product without a variant should have a price'))
    # if self.has_variant is False and self.price == Decimal('0.0'):
    #     raise ValidationError(_('a product without a variant should have price more than 0'))
    # if self.has_variant and self.variant_title == "":
    #     raise ValidationError(_('variant title should be defined'))

    # if self.has_variant and self.variant_set.all().count() == 0:
    #     raise ValidationError(_('variant should be defined'))
    # if self.has_variant:
    #     self.price = Decimal('0.01')
    # else:
    #     self.variant_title = ""
    #     self.variant_set.set(Variant.objects.none())


class Image(models.Model):
    image_file = FilerImageField(related_name='store_product_picture', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    status = models.CharField(max_length=50, choices=STATUS, default='Draft')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(100)))
    comment = models.TextField(max_length=1000)
    title = models.CharField(max_length=100)
    like = models.IntegerField(validators=(MinValueValidator(0),), default=0)
    dislike = models.IntegerField(validators=(MinValueValidator(0),), default=0)
    language = models.CharField(max_length=50, choices=LANGUAGES, default='fa')
    name = models.CharField(max_length=50)
    email = models.EmailField()


# class Variant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
#     price = models.DecimalField(max_digits=12, decimal_places=0)
#     differentiation_value = models.CharField(max_length=200, null=True, blank=True)


class Cart(models.Model):
    CART_STATUS_WAITING = 'W'
    CART_STATUS_TRANSFERRED = 'T'
    CART_STATUS_FAILED = 'F'
    CART_STATUS_CHOICES = [
        (CART_STATUS_WAITING, 'Pending'),
        (CART_STATUS_TRANSFERRED, 'Transferred'),
        (CART_STATUS_FAILED, 'Failed')
    ]
    owner = models.OneToOneField(UserProfile, on_delete=models.RESTRICT, related_name="cart", blank=True, null=True)
    session = models.OneToOneField(Session, on_delete=models.SET_NULL, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CART_STATUS_CHOICES, max_length=20, default=CART_STATUS_WAITING)
    status_change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('id',)

    def __str__(self):
        return f"{self.id}"

    @property
    def get_sum(self):
        return sum((item.quantity * item.product.price) for item in self.cartitem_set.all())

    @property
    def has_item(self):
        return self.cartitem_set.all().count() > 0


class WishItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def get_cartitem_total_price(self):
        return int(self.product.price) * int(self.quantity)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
            self.quantity += cart_item.quantity
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        except CartItem.MultipleObjectsReturned:
            cart_items_sum = CartItem.objects.filter(cart=self.cart, product=self.product).aggregate(Sum('quantity'))
            CartItem.objects.filter(cart=self.cart, product=self.product).delete()
            self.quantity += cart_items_sum["quantity__sum"]
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


class Order(models.Model):
    ORDER_STATUS_WAITING = 'W'
    ORDER_STATUS_TRANSFERRED = 'T'
    ORDER_STATUS_PAYED = 'P'
    ORDER_STATUS_FAILED = 'F'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_WAITING, 'Waiting'),
        (ORDER_STATUS_TRANSFERRED, 'Transferred'),
        (ORDER_STATUS_PAYED, 'Payed'),
        (ORDER_STATUS_FAILED, 'Failed')
    ]

    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name="Orders")
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20, default=ORDER_STATUS_WAITING)

    status_change_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('id',)

    @property
    def total_price(self):
        sum = 0
        for item in self.orderitem_set.all():
            sum += item.product.price * item.quantity
        return sum

    def __str__(self):
        return f"order of {self.owner.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
        ordering = ('id',)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Payment(models.Model):
    STATUS_INITIAL = 1
    STATUS_PROCESSING = 2
    STATUS_CONFIRMED = 3
    STATUS_TYPE_CHOICES = [
        (STATUS_INITIAL, _('initial')),
        (STATUS_PROCESSING, _('processing')),
        (STATUS_CONFIRMED, _('confirmed')),
    ]
    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name="Payment")
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    expired_at = models.DateTimeField(verbose_name=_('expired at'), null=True, blank=True)
    due_at = models.DateTimeField(verbose_name=_('due at'), null=True, blank=True)
    fulfilled_at = models.DateTimeField(verbose_name=_('fulfilled at'), null=True, blank=True)
    amount = models.PositiveIntegerField(default=0, verbose_name=_('amount'))
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS_TYPE_CHOICES,
                                              default=STATUS_PROCESSING)
    status_change_date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    transaction = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ('created_at',)
