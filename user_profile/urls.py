from django.urls import path

from user_profile.views import profile_list_view, profile_update_view

urlpatterns = [
    path('update/', profile_update_view, name="profile_update"),
    path('', profile_list_view, name="profile_list")
]