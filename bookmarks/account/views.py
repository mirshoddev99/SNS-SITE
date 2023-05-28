from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm, ProfileEditForm
from .models import Profile, Contact
from actions.utils import create_action
from actions.models import Action


class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        actions = Action.objects.exclude(user=request.user)
        print(actions)

        following_ids = request.user.following.values_list('id', flat=True)
        print(following_ids)

        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user').prefetch_related('target')[:10]
        return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


class RegisterView(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

    def post(self, request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                if request.user is not AnonymousUser:
                    create_action(request.user, 'has created an account')

                # this message is stored in a cookie
                messages.success(request, 'You have successfully registered')

                return redirect(reverse('login'))

            return render(request, 'account/register.html', {"user_form": user_form})


class UserListView(View, LoginRequiredMixin):
    def get(self, request):
        users = Profile.objects.exclude(username=request.user.username).filter(is_active=True)
        return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


class UserDetailView(View, LoginRequiredMixin):
    def get(self, request, username):
        user = get_object_or_404(Profile, username=username, is_active=True)
        return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = Profile.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


class EditProfileView(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_authenticated:
            profile_form = ProfileEditForm(instance=request.user)
            return render(request, 'account/edit.html', {"profile_form": profile_form})

        return redirect(reverse('account:login'))

    def post(self, request):
        profile_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile was successfully updated")
            return redirect(reverse('account:user_detail', kwargs={'username': request.user.username}))

        messages.error(request, 'An error occurred while updating your profile')
        return render(request, 'account/edit.html', {"profile_form": profile_form})
