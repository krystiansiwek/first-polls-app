from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from polls.models import Question
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for: {username}. You can log in now!')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request,
                  'users/register.html',
                  context
                  )


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,
                                   instance=request.user)

        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account updated!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request,
                  'users/profile.html',
                  context)


class PublicProfile(generic.ListView):
    template_name = 'polls/details.html'
    context_object_name = 'user_questions'

    def get_queryset(self):
        return Question.objects.filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions_author'] = self.kwargs['username']
        context['author_profile'] = Profile.objects.get(user__username=self.kwargs['username'])
        return context
