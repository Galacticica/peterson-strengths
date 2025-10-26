"""
File: views.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: Views for the accounts app.
"""


from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.forms import modelformset_factory
from django.views import View
from . import forms
from . import models


User = get_user_model()

class MyLoginView(LoginView):
    """Custom login view using MyLoginForm."""
    form_class = forms.LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

class MySignupView(FormView):
    """Custom signup view using SignupForm."""
    form_class = forms.SignupForm
    template_name = "accounts/signup.html"
    success_url = "/" 

    def form_valid(self, form):
        user = User.objects.create(
            email=form.cleaned_data["email"],
            username=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password=make_password(form.cleaned_data["password"]), 
        )
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class MyLogoutView(View):
    """Custom logout view."""
    def get(self, request, *args, **kwargs):
        logout(request)  
        return redirect("/")  

def profile_step(request):
    '''
    Handle user profile information step.
    If the profile exists, pre-fill the form with existing data.
    '''

    profile_instance = models.Profile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = forms.ProfileForm(request.POST)
        if form.is_valid():
            profile_data = form.cleaned_data
            if profile_instance:
                for field, value in profile_data.items():
                    setattr(profile_instance, field, value)
                profile_instance.save()
            else:
                profile_instance = models.Profile.objects.create(user=request.user, **profile_data)
            return redirect("experience_step")
    else:
        form = forms.ProfileForm(initial={
            field: getattr(profile_instance, field)
            for field in forms.ProfileForm.base_fields
        } if profile_instance else None)
    return render(request, "accounts/profile_step.html", {"form": form})

def experience_step(request):
    '''
    Handle user experience information step.
    If experience data exists, pre-fill the forms with existing data.
    Uses a formset for previous coaches.
    '''

    PreviousCoachFormSet = modelformset_factory(
        models.PreviousCoach,
        form=forms.PreviousCoachForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    experience_instance = models.Experience.objects.filter(user=request.user).first()

    if request.method == "POST":
        exp_form = forms.ExperienceForm(request.POST)
        coach_formset = PreviousCoachFormSet(request.POST, queryset=models.PreviousCoach.objects.filter(user=request.user))
        if exp_form.is_valid() and coach_formset.is_valid():
            exp_data = exp_form.cleaned_data
            if experience_instance:
                for field, value in exp_data.items():
                    setattr(experience_instance, field, value)
                experience_instance.save()
            else:
                experience_instance = models.Experience.objects.create(user=request.user, **exp_data)
            instances = coach_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in coach_formset.deleted_objects:
                obj.delete()
            return redirect("goal_step")
    else:
        exp_form = forms.ExperienceForm(initial={
            field: getattr(experience_instance, field)
            for field in forms.ExperienceForm.base_fields
        } if experience_instance else None)
        coach_formset = PreviousCoachFormSet(queryset=models.PreviousCoach.objects.filter(user=request.user))

    return render(request, "accounts/experience_step.html", {
        "exp_form": exp_form,
        "coach_formset": coach_formset,
    })


def goal_step(request):
    '''
    Handle user goal information step.
    If goal data exists, pre-fill the form with existing data.
    '''

    GoalFormSet = modelformset_factory(
        models.Goal,
        form=forms.GoalForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    if request.method == "POST":
        goal_formset = GoalFormSet(request.POST, queryset=models.Goal.objects.filter(user=request.user))
        if goal_formset.is_valid():
            instances = goal_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in goal_formset.deleted_objects:
                obj.delete()
            return redirect("next_comp_step")
    else:
        goal_formset = GoalFormSet(queryset=models.Goal.objects.filter(user=request.user))
    return render(request, "accounts/goal_step.html", {"goal_formset": goal_formset})

def next_comp_step(request):
    '''
    Handle user competition information step.
    If the profile exists, pre-fill the form with existing competition data.
    '''

    profile_instance = models.Profile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = forms.CompetitionForm(request.POST)
        if form.is_valid():
            comp_data = form.cleaned_data
            if profile_instance:
                profile_instance.competition_date = comp_data['competition_date']
                profile_instance.desired_weight_class = comp_data['desired_weight_class']
                profile_instance.save()
            else:
                profile_instance = models.Profile.objects.create(
                    user=request.user,
                    competition_date=comp_data['competition_date'],
                    desired_weight_class=comp_data['desired_weight_class']
                )
            return redirect("nutrition_step")  
    else:
        initial_data = {}
        if profile_instance:
            if profile_instance.competition_date:
                initial_data['competition_date'] = profile_instance.competition_date
            if profile_instance.desired_weight_class:
                initial_data['desired_weight_class'] = profile_instance.desired_weight_class
        form = forms.CompetitionForm(initial=initial_data if initial_data else None)
    return render(request, "accounts/next_comp_step.html", {"form": form})


def nutrition_step(request):
    '''
    Handle user nutrition information step.
    If nutrition data exists, pre-fill the form with existing data.
    '''

    nutrition_instance = models.Nutrition.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = forms.NutritionForm(request.POST)
        if form.is_valid():
            nutrition_data = form.cleaned_data
            if nutrition_instance:
                for field, value in nutrition_data.items():
                    setattr(nutrition_instance, field, value)
                nutrition_instance.save()
            else:
                nutrition_instance = models.Nutrition.objects.create(user=request.user, **nutrition_data)
            return redirect("health_step")  
    else:
        form = forms.NutritionForm(initial={
            field: getattr(nutrition_instance, field)
            for field in forms.NutritionForm.base_fields
        } if nutrition_instance else None)
    return render(request, "accounts/nutrition_step.html", {"form": form})


def health_step(request):
    '''
    Handle user health information step.
    If health data exists, pre-fill the forms with existing data.
    Uses a formset for injuries.
    '''

    InjuryFormSet = modelformset_factory(
        models.Injury,
        form=forms.InjuryForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    health_instance = models.Health.objects.filter(user=request.user).first()

    if request.method == "POST":
        health_form = forms.HealthForm(request.POST)
        injury_formset = InjuryFormSet(request.POST, queryset=models.Injury.objects.filter(user=request.user))
        if health_form.is_valid() and injury_formset.is_valid():
            health_data = health_form.cleaned_data
            if health_instance:
                for field, value in health_data.items():
                    setattr(health_instance, field, value)
                health_instance.save()
            else:
                health_instance = models.Health.objects.create(user=request.user, **health_data)
            instances = injury_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in injury_formset.deleted_objects:
                obj.delete()
            return redirect("preference_step")
    else:
        health_form = forms.HealthForm(initial={
            field: getattr(health_instance, field)
            for field in forms.HealthForm.base_fields
        } if health_instance else None)
        injury_formset = InjuryFormSet(queryset=models.Injury.objects.filter(user=request.user))

    return render(request, "accounts/health_step.html", {
        "health_form": health_form,
        "injury_formset": injury_formset,
    })


def preference_step(request):
    '''
    Handle user coaching preference information step.
    If coaching preference data exists, pre-fill the form with existing data.
    '''

    preference_instance = models.CoachingPreference.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = forms.CoachingPreferenceForm(request.POST)
        if form.is_valid():
            preference_data = form.cleaned_data
            if preference_instance:
                for field, value in preference_data.items():
                    setattr(preference_instance, field, value)
                preference_instance.save()
            else:
                preference_instance = models.CoachingPreference.objects.create(user=request.user, **preference_data)
            return redirect("equipment_step")  
    else:
        form = forms.CoachingPreferenceForm(initial={
            field: getattr(preference_instance, field)
            for field in forms.CoachingPreferenceForm.base_fields
        } if preference_instance else None)
    return render(request, "accounts/preference_step.html", {"form": form})

def equipment_step(request):
    '''
    Handle user equipment information step.
    If equipment data exists, pre-fill the forms with existing data.
    Uses a formset for equipment items.
    '''

    EquipmentFormSet = modelformset_factory(
        models.Equipment,
        form=forms.EquipmentForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    profile_instance = models.Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        gear_form = forms.GearForm(request.POST)
        equipment_formset = EquipmentFormSet(request.POST, queryset=models.Equipment.objects.filter(user=request.user))
        if gear_form.is_valid() and equipment_formset.is_valid():
            gear_data = gear_form.cleaned_data
            if profile_instance:
                profile_instance.training_environment = gear_data['training_environment']
                profile_instance.lifting_gear = gear_data['lifting_gear']
                profile_instance.save()
            else:
                profile_instance = models.Profile.objects.create(
                    user=request.user,
                    training_environment=gear_data['training_environment'],
                    lifting_gear=gear_data['lifting_gear']
                )
            instances = equipment_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in equipment_formset.deleted_objects:
                obj.delete()
            return redirect("socials_step")
    else:
        initial_data = {}
        if profile_instance:
            if profile_instance.training_environment:
                initial_data['training_environment'] = profile_instance.training_environment
            if profile_instance.lifting_gear is not None:
                initial_data['lifting_gear'] = profile_instance.lifting_gear
        gear_form = forms.GearForm(initial=initial_data if initial_data else None)
        equipment_formset = EquipmentFormSet(queryset=models.Equipment.objects.filter(user=request.user))

    return render(request, "accounts/equipment_step.html", {
        "gear_form": gear_form,
        "equipment_formset": equipment_formset,
    })

def socials_step(request):
    '''
    Handle user social media information step.
    If social media data exists, pre-fill the forms with existing data.
    Uses a formset for social media links.
    '''

    SocialMediaFormSet = modelformset_factory(
        models.SocialMedia,
        form=forms.SocialMediaForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    if request.method == "POST":
        social_formset = SocialMediaFormSet(request.POST, queryset=models.SocialMedia.objects.filter(user=request.user))
        if social_formset.is_valid():
            instances = social_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in social_formset.deleted_objects:
                obj.delete()
            return redirect("extras_step")  
    else:
        social_formset = SocialMediaFormSet(queryset=models.SocialMedia.objects.filter(user=request.user))
    return render(request, "accounts/socials_step.html", {"social_formset": social_formset})

def extras_step(request):
    '''
    Handle user extras information step.
    If extras data exists, pre-fill the forms with existing data.
    Uses formset for video links.
    '''

    VideoLinkFormSet = modelformset_factory(
        models.VideoLink,
        form=forms.VideoLinkForm,
        extra=1,
        can_delete=True,
        min_num=0,
        validate_min=False
    )
    profile_instance = models.Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        extras_form = forms.ExtrasForm(request.POST)
        video_link_formset = VideoLinkFormSet(request.POST, queryset=models.VideoLink.objects.filter(user=request.user))
        if extras_form.is_valid() and video_link_formset.is_valid():
            extras_data = extras_form.cleaned_data
            if profile_instance:
                profile_instance.recent_training_log = extras_data['recent_training_log']
                profile_instance.save()
            else:
                profile_instance = models.Profile.objects.create(
                    user=request.user,
                    recent_training_log=extras_data['recent_training_log']
                )
            instances = video_link_formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            for obj in video_link_formset.deleted_objects:
                obj.delete()
            return redirect("/")
    else:
        initial_data = {}
        if profile_instance:
            if profile_instance.recent_training_log:
                initial_data['recent_training_log'] = profile_instance.recent_training_log
        extras_form = forms.ExtrasForm(initial=initial_data if initial_data else None)
        video_link_formset = VideoLinkFormSet(queryset=models.VideoLink.objects.filter(user=request.user))

    return render(request, "accounts/extras_step.html", {
        "extras_form": extras_form,
        "video_link_formset": video_link_formset,
    })


def profile_view(request):
    """Render the user's profile page."""
    return render(request, "accounts/profile.html", {"user": request.user})