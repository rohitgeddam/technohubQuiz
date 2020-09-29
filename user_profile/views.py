from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.views.generic import FormView
from .models import Profile
from quizes.models import QuizTaker
from django.urls import reverse_lazy

# Create your views here.

def profile_list_view(request):
    user = request.user
    user_profile = Profile.objects.filter(user=user).first()
    if (user_profile.completed_profile):
        # list view
        # get previously participated quizes
        all_attempted_quizes = user.quiz_takers.all()

        context = {
            "user_profile": user_profile,
            "all_attempted_quizes":all_attempted_quizes,
            }
        return render(request, "user_profile.html", context)
    else:
        return redirect(reverse_lazy('profile_update'))


def profile_update_view(request):
    instance = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.completed_profile = True
        instance.save()
        return redirect(reverse_lazy("profile_list"))
    context = {
        "form": form,
    }
    return render(request, 'profile_update.html', context)
    
    