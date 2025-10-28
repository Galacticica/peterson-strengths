from django.contrib import admin

from .models import Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'rating']
    search_fields = ['author', 'content']
    list_filter = ['rating']