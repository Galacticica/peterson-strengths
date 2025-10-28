"""
File: views.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: View for the about and contact page. 
"""


from django.shortcuts import redirect, render
from .forms import ContactForm


def contact_view(request):
    '''
    Handle contact form submissions and render the contact page.
    '''

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            _send_email(form.cleaned_data, request)
            if request.headers.get("HX-Request"):
                return render(request, "contact/partials/_form_partial.html", {
                    "form": ContactForm(),
                    "success": True
                })
            return redirect("contact")
    else:
        form = ContactForm()
    if request.headers.get("HX-Request"):
        return render(request, "contact/partials/_form_partial.html", {"form": form})
    return render(request, "contact/about.html", {"form": form})
    
def _format_email_body(cleaned_data):
    """Format the email body with submission details."""
    
    return ("A new message has been received from the contact form:\n\n"
        f"Name: {cleaned_data.get('name', '')}\n"
        f"Email: {cleaned_data.get('email', '')}\n"
        f"Message: {cleaned_data.get('message', '')}\n"
    )

def _send_email(cleaned_data, request):
    """Send an email with the contact form submission details."""

    email_body = _format_email_body(cleaned_data)
    print("Sending email with body:\n", email_body)