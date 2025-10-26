"""
File: forms.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: Forms for the contact page.
"""

from django import forms


class ContactForm(forms.Form):
    """Contact form for users to send messages. """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Name", "class": "form-control"}),
        label="Name"
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Email", "class": "form-control"}),
        label="Email"
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Your Message", "class": "form-control", "rows": 5}),
        label="Message"
    )
    