import logging
from abc import ABC

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import get_object_or_404, redirect, resolve_url

from django.urls import reverse_lazy
from django.views import generic

from .admin import UserCreationForm
from .forms import IssueCreateForm, CommentCreateForm, UserUpdateForm
from .models import Issue, Comment, LanveUser

logger = logging.getLogger(__name__)


# Create your views here.
class WelcomeView(generic.TemplateView):
    """Top page for users who is not logged in"""
    template_name = 'lanve/welcome.html'


class SignupView(generic.CreateView):
    """Sign up View"""
    form_class = UserCreationForm
    success_url = reverse_lazy('lanve:signin')

    def post(self, request, *args, **kwargs):
        response = super().post(self)
        # messages.success(self.request, 'Your account was created successfully')
        return response


class MyPasswordResetView(PasswordResetView):
    """set email and send email to reset password View"""
    subject_template_name = 'mailtemplates/password_reset/subject.txt'
    email_template_name = 'mailtemplates/password_reset/message.txt'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('lanve:password_reset_done')


class MyPasswordResetDoneView(PasswordResetDoneView):
    """page which notice that email already sent View"""
    template_name = 'password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """page to input new password View"""
    form_class = SetPasswordForm
    success_url = reverse_lazy('lanve:password_reset_complete')
    template_name = 'password_reset_confirm.html'


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    """page that notice new password set View"""
    template_name = 'password_reset_complete.html'


class ListView(generic.ListView, LoginRequiredMixin):
    """Timeline page with Issue list View"""

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
    """Create new issues View"""
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
    """Details of each issue View"""
    login_url = 'lanve:signin'
    model = Issue
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        """Get the context for this view. for comments"""
        issue_pk = self.kwargs['pk']
        comment = Comment.objects.select_related().filter(issue=issue_pk)
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


class UserDetailView(LoginRequiredMixin, generic.DetailView, ABC):
    """User detail page View"""
    model = LanveUser
    template_name = 'lanve/user_detail.html'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView, ABC):
    """User update page View"""
    model = LanveUser
    form_class = UserUpdateForm
    template_name = 'lanve/user_form.html'

    def get_success_url(self):
        return resolve_url('lanve:user_detail', pk=self.kwargs['pk'])


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Password change View"""
    form_class = PasswordChangeForm
    success_url = reverse_lazy('lanve:password_change_done')
    template_name = 'lanve/user_password_change.html'


class MyPasswordChangeDoneVIew(PasswordChangeDoneView):
    """Password change is done View"""
    template_name = 'lanve/user_password_change_done.html'


class RelatingListView(LoginRequiredMixin, generic.ListView):
    """Lists you are related View"""
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

