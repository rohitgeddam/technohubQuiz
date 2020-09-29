from django.urls import path, include


from .views import HomePageView, QuizStartPage, QuizSubmit, leaderboard, quiz_leaderboard

urlpatterns = [
    path('', HomePageView, name="home_page"),
    
    path('quiz/<slug:slug>/', QuizStartPage, name="quiz_start"),
    path('quiz/<slug:slug>/submit/', QuizSubmit, name="quiz_submit"),
    
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard/<slug:slug>/', quiz_leaderboard, name="quiz_leaderboard")
]