from abc import ABC

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, resolve_url

from django.urls import reverse_lazy, reverse
from django.views import generic

from . import forms, models
from .admin import UserCreationForm
from .forms import IssueCreateForm, CommentCreateForm, UserUpdateForm
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

    def get_context_data(self, **kwargs):
        """Get the context for this view. for comments"""
        issue_pk = self.kwargs['pk']
        comment = Comment.objects.filter(issue=issue_pk)
        context = super().get_context_data(**kwargs)
        context['comments'] = comment
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


# class OnlyYouMixin(UserPassesTestMixin):
#     raise_exception = True
#
#     def see_only_by_myself(self, request):
#         user = self.request.user
#         return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetailView(generic.DetailView, ABC):
    model = LanveUser
    template_name = 'lanve/user_detail.html'


class UserUpdateView(generic.UpdateView, ABC):
    model = LanveUser
    form_class = UserUpdateForm
    template_name = 'lanve/user_form.html'

    def get_success_url(self):
        return resolve_url('lanve:user_detail', pk=self.kwargs['pk'])


class RelatingListView(LoginRequiredMixin, generic.ListView):
    model = Issue  # make html file name as model name + list.html
    ordering = ['-created_at']
    paginate_by = 100
    template_name = 'lanve/issue_relating_list.html'
    login_url = 'lanve:signin'

    def get_queryset(self):
        user_pk = self.request.user.id
        queryset = Issue.objects.select_related().filter(contributor=user_pk) 
        return queryset

    def get_context_data(self, **kwargs):
        """Get the context for this view. for comments"""
        user_pk = self.request.user.id
        queryset = Issue.objects\
            .select_related()\
            .filter(issue__contributor_id=user_pk)\
            .order_by('-created_at')\
            .distinct()
        context = super().get_context_data(**kwargs)
        context['issue_answer_list'] = queryset
        return context

