from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=60)

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


class LoginPage(Page):
    background_image = models.ImageField()


class homePage(Page):
    pass


class Brand(models.Model):
    picture = models.ImageField(upload_to="brand_image")
    brand_name = models.CharField(max_length=60)

    def __str__(self):
        return self.brand_name


class CustomerReviews(models.Model):
    picture = models.ImageField(upload_to="customer")
    review = models.TextField()
    customer_name = models.CharField(max_length=60)


class AboutUsPage(Page):
    is_brand_active = models.BooleanField(default=False)
    brand_title = models.CharField(max_length=100)
    brand_description = models.TextField()
    our_vision_text = models.TextField()
    our_mission_text = models.TextField()
    who_we_are_text_1 = models.TextField()
    who_we_are_text_2 = models.TextField()
    main_picture = models.ImageField(upload_to="about_us")
    who_we_are_picture = models.ImageField(upload_to="who_we_are")
    customer_reviews_title = models.CharField(max_length=100, default="نظرات مشتری های فروشگاه")


class LogoutPage(Page):
    pass


class SignUpPage(Page):
    pass


class ProfilePage(Page):
    pass


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
