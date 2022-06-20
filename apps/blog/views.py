from django.db.models import QuerySet, Q
from django.views.generic import ListView, DetailView

from .models import Post, Category
import datetime
from django.utils import timezone

from ..core.models import BlogPage


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 2

    def get_queryset(self) -> QuerySet:
        category = self.kwargs.get('category')
        search = self.request.GET.get("search")
        queryset = self.model.objects \
            .prefetch_related('comment_set') \
            .order_by('pub_date') \
            .filter(status='Published')
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search) | Q(content2__icontains=search))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = [(category.name, category.post_set.all().count()) for category in categories]
        context['popular_post'] = self.get_queryset().order_by('-view')[:4]
        context['page'] = BlogPage.get_data()
        context['title'] = BlogPage.get_data().title
        context['search'] = self.get_search_parameter()
        return context

    def get_search_parameter(self) -> str:
        parameter = self.request.GET.get("search")
        if parameter:
            return f"&search={parameter}"
        return ""


class Slug(DetailView):
    template_name = 'blog/slug.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_post'] = self.model.objects. \
            order_by('id'). \
            filter(id__gt=self.object.id). \
            first()
        context['prev_post'] = self.model.objects. \
            order_by('id'). \
            filter(id__lt=self.object.id). \
            last()
        context['same_post'] = self.model.objects.order_by('pub_date').filter(status='Published') \
            .filter(category=self.object.category).all()
        return context
