import datetime

from django.db.models import QuerySet, Q, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import CommentForm
from .models import Post, Category, PostViewHistory
from ..core.models import BlogPage


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 6

    def get_queryset(self) -> QuerySet:
        category = self.kwargs.get('category')
        search = self.request.GET.get("search")
        queryset = self.model.objects \
            .prefetch_related('comment_set') \
            .order_by('pub_date') \
            .filter(status='Published')
        if category:
            queryset = queryset.filter(category__slug__iexact=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search) | Q(content2__icontains=search))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = [(category.name, category.slug, category.post_set.all().count()) for category in
                                 categories]
        context['popular_post'] = self.get_popular_posts(4)
        context['page'] = BlogPage.get_data()
        context['title'] = BlogPage.get_data().title
        context['search'] = self.get_search_parameter()
        return context

    def get_search_parameter(self) -> str:
        parameter = self.request.GET.get("search")
        if parameter:
            return f"&search={parameter}"
        return ""

    def get_last_months_date(self, months):
        current_date = datetime.date.today()
        return current_date - datetime.timedelta(days=30 * months)

    def get_popular_posts(self, count):
        return Post.objects.filter(postviewhistory__pub_date__gte=self.get_last_months_date(3)) \
                   .annotate(count=Count('postviewhistory')) \
                   .order_by('-count')[:count]


class Slug(CreateView):
    template_name = 'blog/slug.html'
    post_model = Post
    form_class = CommentForm
    post_obj: Post

    def get_success_url(self):
        return reverse('blog:slug', kwargs={'slug': self.post_obj.slug})

    def get_initial(self):
        self.post_obj = get_object_or_404(self.post_model, slug=self.kwargs.get("slug"))
        return {"post": self.post_obj}

    # def post(self, request, *args, **kwargs):
    #     # self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.log_post_view()
        context['post'] = self.post_obj
        context['comments'] = self.post_obj.comment_set.filter(status='Published')
        context['next_post'] = self.get_next_post()
        context['prev_post'] = self.get_prev_post()
        context['same_post'] = self.get_same_post()
        return context

    def get_same_post(self):
        return self.post_model.objects \
            .order_by('pub_date') \
            .filter(status='Published') \
            .filter(category=self.post_obj.category).all() \
            .exclude(id=self.post_obj.id)

    def get_next_post(self):
        return self.post_model.objects.order_by('id').filter(id__gt=self.post_obj.id).first()

    def get_prev_post(self):
        return self.post_model.objects.order_by('id').filter(id__lt=self.post_obj.id).last()

    def log_post_view(self):
        user = self.request.user if self.request.user.is_authenticated else None
        PostViewHistory.objects.create(
            post=self.post_obj,
            viewer=user
        )
        self.post_obj.view += 1
        self.post_obj.save()
