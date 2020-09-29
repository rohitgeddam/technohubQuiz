from django.shortcuts import redirect
from user_profile.models import Profile
from quizes.models import Quiz
from django.urls import reverse_lazy
from django.utils import timezone

def profile_completion_required():
    def decorator(func):
        def wrap(request, *args, **kwargs):
            profile = Profile.objects.get(user=request.user)
            if (profile.completed_profile):
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy("profile_list"))
        return wrap
    return decorator
    
def quiz_started():
    def decorator(func):
        def wrap(request, *args, **kwargs):
        
            quiz = Quiz.objects.filter(slug=kwargs.get("slug")).first()
            if (quiz.start_time >= timezone.now() and quiz.end_time >= timezone.now()):
            
                return redirect(reverse_lazy("home_page"))
            else:
                return func(request, *args, **kwargs)
           
        return wrap
    return decorator

def quiz_ended():
    def decorator(func):
        def wrap(request, *args, **kwargs):
        
            quiz = Quiz.objects.filter(slug=kwargs.get("slug")).first()
            if (quiz.end_time <= timezone.now()):
            
                return redirect(reverse_lazy("home_page"))
            else:
                return func(request, *args, **kwargs)
           
        return wrap
    return decorator