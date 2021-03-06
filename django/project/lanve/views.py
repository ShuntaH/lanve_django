import logging
from abc import ABC

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import get_object_or_404, redirect, resolve_url

from django.urls import reverse_lazy, reverse
from django.views import generic
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .admin import UserCreationForm
from .forms import IssueCreateForm, CommentCreateForm, UserUpdateForm
from .models import Issue, Comment, LanveUser

logger = logging.getLogger(__name__)


# Create your views here.


class WelcomeView(generic.TemplateView):
    """ Top page for users who is not logged in """
    template_name = 'lanve/welcome.html'


class SignupView(generic.CreateView):
    """ Sign up View """

    form_class = UserCreationForm
    success_url = reverse_lazy('lanve:signin')

    def post(self, request, *args, **kwargs):
        response = super().post(self)
        # messages.success(self.request, 'Your account was created successfully')
        return response


class MyPasswordResetView(PasswordResetView):
    """ Set email and send email to reset password View """

    subject_template_name = 'mailtemplates/password_reset/subject.txt'
    email_template_name = 'mailtemplates/password_reset/message.txt'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('lanve:password_reset_done')


class MyPasswordResetDoneView(PasswordResetDoneView):
    """ Page which notice that email already sent View """

    template_name = 'password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """ Page to input new password View """

    form_class = SetPasswordForm
    success_url = reverse_lazy('lanve:password_reset_complete')
    template_name = 'password_reset_confirm.html'


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    """ Page that notice new password set View """

    template_name = 'password_reset_complete.html'


class ListView(generic.ListView, LoginRequiredMixin):
    """ Timeline page with Issue list View """

    model = Issue  # make html file name as model name + list.html
    ordering = ['-created_at']
    paginate_by = 100
    login_url = 'lanve:signin'

    def get_queryset(self):
        user_mother_tongue = self.request.user.mother_tongue
        queryset = Issue.objects \
            .select_related() \
            .filter(language_to=user_mother_tongue) \
            .order_by('-created_at')

        # keyword = self.request.GET.get('keyword')
        # if keyword:
        #     queryset = queryset.filter(
        #         Q(title__icontains=keyword) | Q(text__icontains=keyword)
        #
        #     )
        return queryset


class AddView(LoginRequiredMixin, generic.CreateView):
    """ Create new issues View """

    model = Issue
    form_class = IssueCreateForm
    login_url = 'lanve:signin'
    success_url = reverse_lazy('lanve:list')

    def form_valid(self, form):
        messages.success(self.request, 'Your issue was posted successfully')
        issue = form.save(commit=False)
        issue.contributor = self.request.user
        issue.save()
        response = super().form_valid(form)
        return response


class DetailView(LoginRequiredMixin, generic.DetailView, generic.edit.ModelFormMixin):
    """ Details of each issue View """

    login_url = 'lanve:signin'
    model = Issue
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        """
        Get the context of comments for this view.
        Handle to calculate the number of views of this issue.
        """

        # Count the number of views
        issue = self.get_object()
        issue.count_view += 1
        issue.save()

        # get comment queryset of the issue
        issue_pk = self.kwargs['pk']
        comment = Comment.objects.select_related() \
            .filter(issue=issue_pk)
        #     .annotate(
        #     favorite_count=Count('likes')
        # )

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

        # save
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
    """ User detail page View """

    model = LanveUser
    template_name = 'lanve/user_detail.html'
    login_url = 'lanve:signin'

    def get_context_data(self, **kwargs):
        """ Get the context for this view. for comments """

        user_pk = self.kwargs['pk']
        queryset_issue_commented = Issue.objects \
            .select_related() \
            .filter(issue__contributor_id=user_pk) \
            .order_by('-created_at') \
            .distinct()
        queryset_issue = Issue.objects \
            .select_related() \
            .filter(contributor=user_pk) \
            .order_by('-updated_at')
        context = super().get_context_data(**kwargs)
        context['issue_list'] = queryset_issue
        context['issue_commented_list'] = queryset_issue_commented
        return context


class UserUpdateView(LoginRequiredMixin, generic.UpdateView, ABC):
    """ User update page View """

    model = LanveUser
    form_class = UserUpdateForm
    template_name = 'lanve/user_form.html'

    def get_success_url(self):
        return resolve_url('lanve:user_detail', pk=self.kwargs['pk'])


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """ Password change View """

    form_class = PasswordChangeForm
    success_url = reverse_lazy('lanve:password_change_done')
    template_name = 'lanve/user_password_change.html'
    login_url = 'lanve:signin'


class MyPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """ Password change is done View """

    template_name = 'lanve/user_password_change_done.html'
    login_url = 'lanve:signin'


def get_absolute_url(self):
    issue_pk = self.issue.pk
    return reverse("lanve:detail", kwargs={"issue_pk": issue_pk})


class LikeComment(APIView):
    """ API for like button of each comments """

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        comment_like_obj = get_object_or_404(Comment, pk=self.kwargs['comment_pk'], )
        url_ = get_absolute_url
        status = request.GET.getlist('status')
        status = bool(int(status[0]))
        user = self.request.user
        if user in comment_like_obj.like.all():
            if not (status):
                liked = True
            else:
                comment_like_obj.like.remove(user)
                liked = False
        else:
            if not (status):
                liked = False
            else:
                comment_like_obj.like.add(user)
                liked = True
        data = {
            "liked": liked,
        }
        return Response(data)
