from django.views.generic import ListView, DetailView

from .models import Post, Category


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 2

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category:
            return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = [(category.name, category.post_set.all().count()) for category in categories]
        return context


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
