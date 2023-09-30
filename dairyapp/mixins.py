from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import redirect

class PaginationMixin:
    def paginate_queryset(self,queryset,page_size):
        try:
            return super().paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super().paginate_queryset(queryset,page_size)


    