from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date
from django.shortcuts import render
from django.urls import reverse_lazy
from Activities.models import Event, Course
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from django.utils import timezone
from datetime import date

def aboutAs_view(request):
    context = {'title': 'About Us - SpritzCollege'}
    return render(request, 'about.html', context)

class CustomLoginView(LoginView):
    
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('auth') == 'notok':
            messages.info(request, "You do not have permission to access this page. Please login with appropriate credentials.")
            return redirect('home')
        
        if request.user.is_authenticated:
            messages.info(request, f'You have already logged in as {request.user.username}!')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

def go_home(request):
    today = date.today()
    latest_courses = Course.objects.filter(end_date__gte=today).order_by('-end_date')[:5]
    
    if request.user.is_authenticated:
        user_events = Event.objects.filter(
            bookings__user=request.user, 
            date__gte=timezone.now()
        ).order_by('date')
        
        user_courses = Course.objects.filter(
            subscribers__user=request.user, 
            start_date__gte=timezone.now().date()
        ).order_by('start_date')
    else:
        user_events = []
        user_courses = []
    
    ctx = {
        "title": "Home",
        "events_list": Event.objects.all(),
        "courses_list": Course.objects.all(),
        "latest_events": Event.objects.order_by('date')[:5],
        "latest_courses": latest_courses,
        "user_events": user_events,
        "user_courses": user_courses,
    }
    return render(request, template_name="index.html", context=ctx)