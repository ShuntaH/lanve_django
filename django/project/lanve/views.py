from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from .admin import UserCreationForm
from .models import Issue


class WelcomeView(generic.TemplateView):
    template_name = 'welcome.html'


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('lanve:signin')

    def post(self, request, *args, **kwargs):
        response = super().post(self)
        # messages.success(self.request, 'Your account was created successfully')
        return response


class ListView(generic.ListView):
    model = Issue
    paginate_by = 8
    # login_url = '/buybuy/signin/'
