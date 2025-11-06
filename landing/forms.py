"""
File: forms.py
Author: Reagan Zierke
Date: 2025-11-05
Description: description
"""

from django import forms

class InterestedPersonForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    email = forms.EmailField(label="Email Address")

    
