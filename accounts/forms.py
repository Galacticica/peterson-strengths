from django import forms
from django.contrib.auth import authenticate as auth_authenticate
from .models import PreviousCoach, Goal, Injury, Equipment, VideoLink, SocialMedia


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
        label="Email"
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}),
        label="Password"
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    def clean(self):
        self.user_cache = auth_authenticate(
           self.request,
           username=self.cleaned_data.get("email"),
              password=self.cleaned_data.get("password")
        )
        if self.user_cache is None:
           raise forms.ValidationError("Invalid email or password.")
        return super().clean()
    def get_user(self):
        return self.user_cache
    

class SignupForm(forms.Form):

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
        label="Email"
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"}),
        label="Confirm Password"
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
        label="Last Name"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class ProfileForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "form-control"}),
        label="Phone Number"
    )
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"placeholder": "Date of Birth (YYYY-MM-DD)", "class": "form-control"}),
        label="Date of Birth"
    )
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Gender"
    )
    height = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Height (inches)", "class": "form-control"}),
        label="Height (inches)"
    )
    weight = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Weight (pounds)", "class": "form-control"}),
        label="Weight (pounds)"
    )
    location = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Location", "class": "form-control"}),
        label="Location"
    )
    timezone = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Timezone", "class": "form-control"}),
        label="Timezone"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ExperienceForm(forms.Form):
    level = forms.ChoiceField(
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Experience Level"
    )
    time_lifted = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Time Lifted (e.g., '6 months', '2 years')", "class": "form-control"}),
        label="Time Lifted"
    )
    current_program = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Current Training Split / Program", "class": "form-control"}),
        label="Current Program"
    )
    days_per_week = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Preferred Days per Week", "class": "form-control"}),
        label="Days per Week"
    )
    preffered_days = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Preferred Training Days", "class": "form-control"}),
        label="Preferred Days"
    )
    squat_est = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Estimated Squat 1RM", "class": "form-control"}),
        label="Estimated Squat 1RM"
    )
    bench_est = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Estimated Bench Press 1RM", "class": "form-control"}),
        label="Estimated Bench Press 1RM"
    )
    deadlift_est = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Estimated Deadlift 1RM", "class": "form-control"}),
        label="Estimated Deadlift 1RM"
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CompetitionForm(forms.Form):
    competition_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"placeholder": "Competition Date (YYYY-MM-DD)", "class": "form-control"}),
        label="Competition Date"
    )
    desired_weight_class = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Desired Weight Class", "class": "form-control"}),
        label="Desired Weight Class"
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class NutritionForm(forms.Form):
    plan = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Do you have a nutrition plan?"
    )
    calories_per_day = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Calories per Day", "class": "form-control"}),
        label="Calories per Day"
    )
    protein_per_day = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Protein per Day (grams)", "class": "form-control"}),
        label="Protein per Day (grams)"
    )
    weight_management = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Weight Management Goals", "class": "form-control"}),
        label="Current Weight Management Goal (e.g. cutting, bulking, maintenance)"
    )
    sleep_habits = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Sleep Habits (hours per night)", "class": "form-control"}),
        label="Sleep Habits (hours per night)"
    )
    stress = forms.ChoiceField(
        choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Stress Level"
    )
    supplements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Supplements Used", "class": "form-control", "rows": 3}),
        label="Supplements Used (if any)"
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class HealthForm(forms.Form):
    conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "List any health conditions", "class": "form-control", "rows": 3}),
        label="Health Conditions"
    )
    mobility_issues = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "List any mobility issues", "class": "form-control", "rows": 3}),
        label="Mobility Issues"
    )
    cleared_for_training = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Cleared for Training"
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CoachingPreferenceForm(forms.Form):
    style = forms.ChoiceField(
        choices=[('hands_on', 'Hands-on'), ('hands_off', 'Hands-off'), ('balanced', 'Balanced')],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Coaching Style"
    )
    check_in_frequency = forms.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Biweekly'), ('monthly', 'Monthly')],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Check-in Frequency"
    )
    video_analysis = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Include Video Analysis"
    )
    communication_method = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Preferred Communication Method", "class": "form-control"}),
        label="Communication Method"
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class GearForm(forms.Form):
    training_environment = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Training Environment", "class": "form-control"}),
        label="Training Environment (e.g., home gym, commercial gym)"
    )
    lifting_gear = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Do you use lifting gear? (e.g., belts, wraps)"
    )

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'link']
        widgets = {
            'platform': forms.Select(attrs={"class": "form-control"}),
            'link': forms.URLInput(attrs={"placeholder": "Social Media Link URL", "class": "form-control"}),
        }

class PreviousCoachForm(forms.ModelForm):
    class Meta:
        model = PreviousCoach
        fields = ['coach_name']
        widgets = {
            'coach_name': forms.TextInput(attrs={"placeholder": "Coach Name", "class": "form-control"}),
        }
    
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['type', 'description']
        widgets = {
            'type': forms.Select(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"placeholder": "Goal Description", "class": "form-control", "rows": 3}),
        }

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ['started', 'ended', 'info']
        widgets = {
            'started': forms.DateInput(attrs={"placeholder": "Start Date (YYYY-MM-DD)", "class": "form-control"}),
            'ended': forms.DateInput(attrs={"placeholder": "End Date (YYYY-MM-DD)", "class": "form-control"}),
            'info': forms.Textarea(attrs={"placeholder": "Injury Information", "class": "form-control", "rows": 3}),
        }

class VideoLinkForm(forms.ModelForm):
    class Meta:
        model = VideoLink
        fields = ['link']
        widgets = {
            'link': forms.URLInput(attrs={"placeholder": "Video Link URL", "class": "form-control"}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['piece_name']
        widgets = {
            'piece_name': forms.TextInput(attrs={"placeholder": "Equipment Name", "class": "form-control"}),
        }