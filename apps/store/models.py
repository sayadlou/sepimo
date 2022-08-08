from decimal import Decimal
from uuid import uuid4

from azbankgateways.models import Bank
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from tinymce.models import HTMLField

from apps.account.models import UserProfile, Address
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


class ProductManager(models.Manager):

    def get_queryset(self):
        # return super().get_queryset()
        return super().get_queryset().select_related("introduction_picture", "category", "brand")


class Product(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    STOCK_AVAILABILITY = {
        "low_in_stock": 3,
        "out_of_stock": 1,
    }
    STOCK_AVAILABILITY_LABEL = {
        "available": _("Available"),
        "low": _("Low in stock"),
        "out": _("Out of stock"),
    }
    objects = ProductManager()
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
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    maximum_order_quantity = models.PositiveIntegerField(default=10)

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

    @property
    def stock_label(self) -> str:
        return Product.STOCK_AVAILABILITY_LABEL[self.stock_status]

    @property
    def stock_status(self) -> str:
        if self.stock_inventory > Product.STOCK_AVAILABILITY["low_in_stock"]:
            return "available"
        elif Product.STOCK_AVAILABILITY["low_in_stock"] >= self.stock_inventory > Product.STOCK_AVAILABILITY[
            "out_of_stock"]:
            return "low"
        else:
            return "out"


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


class CartManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related("cartitem_set")


class Cart(models.Model):
    CART_STATUS_WAITING = 'W'
    CART_STATUS_TRANSFERRED = 'T'
    CART_STATUS_FAILED = 'F'
    CART_STATUS_CHOICES = [
        (CART_STATUS_WAITING, 'Pending'),
        (CART_STATUS_TRANSFERRED, 'Transferred'),
        (CART_STATUS_FAILED, 'Failed')
    ]
    objects = CartManager()
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="cart", blank=True, null=True)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CART_STATUS_CHOICES, max_length=20, default=CART_STATUS_WAITING)
    status_change_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('id',)

    def __str__(self):
        return f"{self.id}"

    @property
    def get_sum(self):
        oder_sum_dict = self.cartitem_set.aggregate(total=Sum(F('product__price') * F('quantity')))
        return oder_sum_dict['total'] if oder_sum_dict['total'] else 0
        # return sum((item.quantity * item.product.price) for item in self.cartitem_set.all())

    @property
    def has_item(self):
        return self.cartitem_set.all().count() > 0


class WishItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def get_cartitem_total_price(self):
        return int(self.product.price) * int(self.quantity)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


def one_month_later():
    return timezone.now() + timezone.timedelta(days=30)


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=0)
    expiration_date = models.DateField(default=one_month_later)
    minimum_purchase_amount = models.PositiveIntegerField(default=100000)
    discount_purchase_amount = models.PositiveIntegerField(default=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Shipping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    shipping_title = models.CharField(max_length=100)
    shipping_coast = models.PositiveIntegerField(default=10000)
    delivery_time = models.PositiveIntegerField(default=2)
    minimum_order_cost = models.PositiveIntegerField(default=10000)


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

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name="Orders")
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    shipping = models.ForeignKey(Shipping, on_delete=models.RESTRICT)
    discount = models.ForeignKey(Discount, on_delete=models.RESTRICT, null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20, default=ORDER_STATUS_WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    status_change_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('status_change_date',)

    @property
    def total_price(self):
        oder_sum_dict = self.orderitem_set.aggregate(Sum('product_price'))
        return oder_sum_dict.get('product_price__sum', 0)

    def __str__(self):
        return f"order of {self.owner.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
        ordering = ('id',)

#
# class Payment(models.Model):
#     STATUS_INITIAL = 1
#     STATUS_PROCESSING = 2
#     STATUS_CONFIRMED = 3
#     STATUS_TYPE_CHOICES = [
#         (STATUS_INITIAL, _('initial')),
#         (STATUS_PROCESSING, _('processing')),
#         (STATUS_CONFIRMED, _('confirmed')),
#     ]
#     owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name="Payment")
#     order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
#     expired_at = models.DateTimeField(verbose_name=_('expired at'), null=True, blank=True)
#     due_at = models.DateTimeField(verbose_name=_('due at'), null=True, blank=True)
#     fulfilled_at = models.DateTimeField(verbose_name=_('fulfilled at'), null=True, blank=True)
#     amount = models.PositiveIntegerField(default=0, verbose_name=_('amount'))
#     status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS_TYPE_CHOICES,
#                                               default=STATUS_PROCESSING)
#     status_change_date = models.DateTimeField(auto_now=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     transaction = GenericForeignKey('content_type', 'object_id')
#
#     class Meta:
#         verbose_name = _('Payment')
#         verbose_name_plural = _('Payments')
#         ordering = ('created_at',)
