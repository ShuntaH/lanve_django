from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views import generic

from . import forms, models
from .admin import UserCreationForm
from .forms import IssueCreateForm, CommentCreateForm
from .models import Issue, Comment


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
    ordering = ['-created_at']
    paginate_by = 100
    login_url = 'lanve:signin'

    # def get_queryset(self):
    #     queryset = Issue.objects.all().order_by('-created_at')  # 新しい投稿順
    #     keyword = self.request.GET.get('keyword')
    #     if keyword:
    #         queryset = queryset.filter(
    #             Q(title__icontains=keyword) | Q(text__icontains=keyword)
    #
    #         )
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class AddView(LoginRequiredMixin, generic.CreateView):
    model = Issue
    form_class = IssueCreateForm
    login_url = 'lanve:signin'
    success_url = reverse_lazy('lanve:list')

    def form_valid(self, form):
        messages.success(self.request, 'Your issue was posted successfully')
        issue = form.save(commit=False)
        form.instance.user = self.request.user
        user = form.instance.user
        issue.contributor = user
        issue.save()
        response = super().form_valid(form)
        return response


class DetailView(LoginRequiredMixin, generic.DetailView, generic.edit.ModelFormMixin):
    login_url = 'lanve:signin'
    model = Issue
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        """Get the context for this view."""
        issue_pk = self.kwargs['pk']
        comment_queryset = Comment.objects.all().filter(contributor=issue_pk)
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_list': comment_queryset
        })
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = CommentCreateForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                form_comment = form.save(commit=False)
                form_comment.issue = models.Issue.objects.get(pk=self.kwargs['pk'])
                form_comment.contributor = models.LanveUser.objects.get(pk=1)
                # 保存
                form_comment.save()
                # redirect to a new URL:
                self.form_valid(form)
            else:
                self.form_invalid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def form_valid(self, form):
        return HttpResponseRedirect(reverse_lazy('lanve:detail', kwargs={'pk': self.kwargs['pk']}))









