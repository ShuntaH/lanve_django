from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .admin import UserCreationForm
from .models import Issue


# Create your views here.

class WelcomeView(generic.TemplateView):
    template_name = 'lanve/welcome.html'


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('lanve:signin')

    def post(self, request, *args, **kwargs):
        response = super().post(self)
        # messages.success(self.request, 'Your account was created successfully')
        return response


class ListView(generic.ListView, LoginRequiredMixin):
    model = Issue  # make html file name as model name + list.html
    paginate_by = 100
    login_url = 'lanve:signin'

    def get_queryset(self):
        queryset = Issue.objects.all().order_by('-created_at')  # 新しい投稿順
        # keyword = self.request.GET.get('keyword')
        # if keyword:
        #     queryset = queryset.filter(
        #         Q(title__icontains=keyword) | Q(text__icontains=keyword)
        #
        #     )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
