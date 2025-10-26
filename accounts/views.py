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

    PreviousCoachFormSet = modelformset_factory(models.PreviousCoach, form=forms.PreviousCoachForm, extra=1, can_delete=True)
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
            return redirect("contact")
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



