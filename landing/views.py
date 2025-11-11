from django.shortcuts import render
from django.http import HttpResponse
from .forms import InterestedPersonForm
from .models import InterestedPerson


def landing_view(request):
    form = InterestedPersonForm()
    if request.method == "POST":
        form = InterestedPersonForm(request.POST)
        if form.is_valid():
            InterestedPerson.objects.create(**form.cleaned_data)
            if request.headers.get('HX-Request'):
                return HttpResponse("""
                    <form id="signup-form" method="post" hx-post="" hx-swap="outerHTML" hx-target="#form-container" class="bg-base-100 p-6 rounded-lg shadow">
                        <input type="hidden" name="csrfmiddlewaretoken" value="%s">
                        <div class="grid gap-4">
                            <div>
                                <label for="id_first_name" class="block mb-1">First name</label>
                                <input id="id_first_name" name="first_name" type="text" required maxlength="30" class="input input-bordered w-full" placeholder="Jane">
                            </div>
                            <div>
                                <label for="id_last_name" class="block mb-1">Last name</label>
                                <input id="id_last_name" name="last_name" type="text" required maxlength="30" class="input input-bordered w-full" placeholder="Doe">
                            </div>
                            <div>
                                <label for="id_email" class="block mb-1">Email</label>
                                <input id="id_email" name="email" type="email" required class="input input-bordered w-full" placeholder="you@example.com">
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-full mt-6">Get updates</button>
                    </form>
                    <div class="alert alert-success mt-4" id="success-message">
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>Thank you for signing up! We'll keep you updated.</span>
                    </div>
                    <script>
                        setTimeout(function() {
                            var msg = document.getElementById('success-message');
                            if (msg) {
                                msg.style.transition = 'opacity 0.5s';
                                msg.style.opacity = '0';
                                setTimeout(function() { msg.remove(); }, 500);
                            }
                        }, 5000);
                    </script>
                """ % request.POST.get('csrfmiddlewaretoken'))
            form = InterestedPersonForm()
        else:
            if request.headers.get('HX-Request'):
                error_html = '<form id="signup-form" method="post" hx-post="" hx-swap="outerHTML" hx-target="#form-container" class="bg-base-100 p-6 rounded-lg shadow">'
                error_html += f'<input type="hidden" name="csrfmiddlewaretoken" value="{request.POST.get("csrfmiddlewaretoken")}">'
                
                if form.non_field_errors():
                    error_html += '<div class="mb-3 text-sm text-error">' + ', '.join(form.non_field_errors()) + '</div>'
                
                error_html += '<div class="grid gap-4">'
                
                for field_name in ['first_name', 'last_name', 'email']:
                    field = form[field_name]
                    error_html += '<div>'
                    error_html += f'<label for="id_{field_name}" class="block mb-1">{field.label}</label>'
                    error_html += f'<input id="id_{field_name}" name="{field_name}" type="{field.field.widget.input_type}" '
                    if field.field.required:
                        error_html += 'required '
                    if hasattr(field.field, 'max_length') and field.field.max_length:
                        error_html += f'maxlength="{field.field.max_length}" '
                    error_html += f'class="input input-bordered w-full" placeholder="{field.field.widget.attrs.get("placeholder", "")}" value="{field.value() or ""}">'
                    if field.errors:
                        error_html += f'<p class="text-sm text-error mt-1">{", ".join(field.errors)}</p>'
                    error_html += '</div>'
                
                error_html += '</div>'
                error_html += '<button type="submit" class="btn btn-primary w-full mt-6">Get updates</button>'
                error_html += '</form>'
                
                return HttpResponse(error_html)
    
    return render(request, 'landing/land.html', {'form': form})