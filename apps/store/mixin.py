class AjaxMixin:
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return super().ajax_get(self, request, *args, **kwargs)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return super().ajax_post(self, request, *args, **kwargs)
        return super().post(self, request, *args, **kwargs)

    # is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
