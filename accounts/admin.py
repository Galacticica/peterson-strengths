from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import accounts.models as models

admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Experience)
admin.site.register(models.PreviousCoach)
admin.site.register(models.Nutrition)
admin.site.register(models.Goal)
admin.site.register(models.Injury)
admin.site.register(models.CoachingPreference)
admin.site.register(models.Equipment)
admin.site.register(models.VideoLink)
admin.site.register(models.SocialMedia)
