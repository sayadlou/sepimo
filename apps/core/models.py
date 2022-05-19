from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField


# Create your models here.
from tinymce.models import HTMLField


class Page(models.Model):
    title = models.CharField(max_length=60, default="Sepimo")

    class Meta:
        abstract = True

    @classmethod
    def get_setting(cls):
        try:
            return cls.objects.get(id__gt=0)

        except(cls.DoesNotExist, cls.MultipleObjectsReturned):
            raise Http404(_('Settings for this page not found'))

    def clean(self):
        model = type(self)
        if model.objects.all().count() >= 1 and model.objects.get(id__gt=0).pk != self.pk:
            raise ValidationError(_("add setting Error"))


class homePage(Page):
    pass


class Brand(models.Model):
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


class SignUpPage(Page):
    background_image = FilerImageField(related_name='signup_page', on_delete=models.PROTECT)


class LoginPage(Page):
    background_image = FilerImageField(related_name='login_page', on_delete=models.PROTECT)


class PasswordChangePage(Page):
    pass


class PasswordChangeDonePage(Page):
    pass


class PasswordResetPage(Page):
    pass


class PasswordResetDonePage(Page):
    pass


class PasswordResetFormPage(Page):
    pass


class PasswordResetCompletePage(Page):
    pass


class BlogIndexPage(Page):
    pass


class BlogSlugPage(Page):
    pass


class BlogCategoryPage(Page):
    pass


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
