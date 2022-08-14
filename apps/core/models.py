from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField

from tinymce.models import HTMLField


class Page(models.Model):
    title = models.CharField(max_length=60, default="Sepimo")

    class Meta:
        abstract = True

    @classmethod
    def get_data(cls):
        try:
            return cls.objects.get(id__gt=0)

        except(cls.DoesNotExist, cls.MultipleObjectsReturned):
            raise Http404(_('Settings for this page not found'))

    def clean(self):
        model = type(self)
        if model.objects.all().count() >= 1 and model.objects.get(id__gt=0).pk != self.pk:
            raise ValidationError(_("add setting Error"))


class HomePage(Page):
    pass


class BrandPage(Page):
    picture = FilerImageField(related_name='brand_image', on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=60)

    def __str__(self):
        return self.brand_name


class CustomerReviews(models.Model):
    picture = FilerImageField(related_name='customer', on_delete=models.PROTECT)
    review = models.TextField()
    customer_name = models.CharField(max_length=60)


class AboutUsPage(Page):
    is_brand_active = models.BooleanField(default=False)
    brand_title = models.CharField(max_length=100)
    brand_description = HTMLField()
    our_vision_text = HTMLField()
    our_mission_text = HTMLField()
    who_we_are_text_1 = HTMLField()
    who_we_are_text_2 = HTMLField()
    main_picture = FilerImageField(related_name='about_us', on_delete=models.PROTECT)
    who_we_are_picture = FilerImageField(related_name='who_we_are', on_delete=models.PROTECT)
    customer_reviews_title = models.CharField(max_length=100, default="نظرات مشتری های فروشگاه")


class ProfilePage(Page):
    header_text_big = models.CharField(max_length=60)
    header_text_small = models.CharField(max_length=60)
    header_background = FilerImageField(related_name='profile_background', on_delete=models.PROTECT)
    menu_dashboard = models.CharField(max_length=60, default="داشبورد")
    menu_orders = models.CharField(max_length=60, default="سفارشات")
    menu_address = models.CharField(max_length=60, default="آدرس")
    menu_profile = models.CharField(max_length=60, default="جزئیات حساب کاربری")
    menu_password_change = models.CharField(max_length=60, default="تغییر گذرواژه")
    menu_logout = models.CharField(max_length=60, default="خروج از حساب کاربری")


class SignPage(Page):
    background_image = FilerImageField(related_name='signup_page', on_delete=models.PROTECT)


class PasswordResetPage(Page):
    background_image = FilerImageField(related_name='password_reset_page', on_delete=models.PROTECT)
    text_head = models.CharField(max_length=200, default="did you forget your password?")
    text_help = models.CharField(max_length=200, default="enter your email to reset your password")
    password_sent_message = models.TextField(max_length=300,
                                             default="We've emailed you instructions for setting your password, if an "
                                                     "account exists with the email you entered. You should receive "
                                                     "them shortly. If you don't receive an email, please make sure "
                                                     "you've entered the address you registered with,and check your "
                                                     "spam folder."
                                             )


class BlogPage(Page):
    about_blog_active = models.BooleanField(default=False)
    about_blog_title = models.CharField(max_length=50, null=True, blank=True)
    about_blog_text = models.TextField(max_length=200, null=True, blank=True)


class ContactUsPage(Page):
    pass


class ContactUsThanksPage(Page):
    pass


class CartPage(Page):
    pass


class OrdersPage(Page):
    pass


class PaymentPage(Page):
    pass
