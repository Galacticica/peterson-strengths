from django.shortcuts import render
from .forms import InterestedPersonForm
from .models import InterestedPerson


def landing_view(request):
    form = InterestedPersonForm()
    if request.method == "POST":
        form = InterestedPersonForm(request.POST)
        if form.is_valid():
            InterestedPerson.objects.create(**form.cleaned_data)
            form = InterestedPersonForm()
    return render(request, 'landing/land.html', {'form': form})