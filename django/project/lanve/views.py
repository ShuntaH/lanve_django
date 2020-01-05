from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views import generic

from . import forms, models
from .admin import UserCreationForm
from .forms import IssueCreateForm, CommentCreateForm
from .models import Issue, Comment, LanveUser


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
    pk = None

    def get_context_data(self, **kwargs):
        """Get the context for this view."""
        issue_pk = self.kwargs['pk']
        comment = Comment.objects.all().filter(issue=issue_pk)
        context = super().get_context_data(**kwargs)
        context['comment_list'] = comment
        return context

    def form_valid(self, form):
        # process the data in form.cleaned_data as required
        issue_pk = self.kwargs['pk']
        contributor_pk = self.request.user.id
        comment = form.save(commit=False)
        comment.issue = get_object_or_404(Issue, pk=issue_pk)
        comment.contributor = get_object_or_404(LanveUser, pk=contributor_pk)
        # 保存
        comment.save()
        return redirect('lanve:detail', pk=issue_pk)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # create a form instance and populate it with data from the request:
        form = self.get_form()
        # check whether it's valid:
        if form.is_valid():
            # redirect to a new URL:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
