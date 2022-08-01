from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def print_fild(context, counter, arg=None):
    print(context["product_pic_url"][0], counter)
    url = context["product_pic_url"][counter]
    return mark_safe(f'<img src="/media/{url}">')
