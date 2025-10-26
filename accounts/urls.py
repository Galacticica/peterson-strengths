from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.MyLoginView.as_view(), name="login_page"),
    path("signup/", views.MySignupView.as_view(), name="signup_page"),
    path("logout/", views.MyLogoutView.as_view(), name="logout_page"),
    path("profile/", views.profile_step, name="profile_step"),
    path("experience/", views.experience_step, name="experience_step"),
    path("goals/", views.goal_step, name="goal_step"),
    path("competition/", views.next_comp_step, name="next_comp_step"),
    path("nutrition/", views.nutrition_step, name="nutrition_step"),
    path("health/", views.health_step, name="health_step"),
    path("preference/", views.preference_step, name="preference_step"),
]
