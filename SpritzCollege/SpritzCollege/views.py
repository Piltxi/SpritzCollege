from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomUserLoginForm

from datetime import date
from django.shortcuts import render
from Activities.models import Event, Course

def custom_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('home')
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

def go_home (request):

    today = date.today()
    latest_courses = Course.objects.filter(end_date__gte=today).order_by('-end_date')[:5]
    print(f"Dimensione: {Event.objects.all().count()}")

    ctx = {"title":"Home", "events_list": Event.objects.all(), "courses_list": Course.objects.all(), "latest_events": Event.objects.order_by('date')[:5], "latest_courses": latest_courses}
    return render(request, template_name="index.html", context=ctx)

def go_control_panel (request): 
    return render(request, template_name="control_panel.html")