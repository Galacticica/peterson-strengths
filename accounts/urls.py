from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.MyLoginView.as_view(), name="login_page"),
    path("signup/", views.MySignupView.as_view(), name="signup_page"),
    path("logout/", views.MyLogoutView.as_view(), name="logout_page"),
    path("profile/edit/personal/", views.profile_step, name="profile_step"),
    path("profile/edit/experience/", views.experience_step, name="experience_step"),
    path("profile/edit/goals/", views.goal_step, name="goal_step"),
    path("profile/edit/competition/", views.next_comp_step, name="next_comp_step"),
    path("profile/edit/nutrition/", views.nutrition_step, name="nutrition_step"),
    path("profile/edit/health/", views.health_step, name="health_step"),
    path("profile/edit/preference/", views.preference_step, name="preference_step"),
    path("profile/edit/equipment/", views.equipment_step, name="equipment_step"),
    path("profile/edit/socials/", views.socials_step, name="socials_step"),
    path("profile/edit/extras/", views.extras_step, name="extras_step"),
    path("profile/", views.profile_view, name="profile_page"),
]
