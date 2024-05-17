from datetime import date
from django.shortcuts import render
from Activities.models import Event, Course

def go_home (request):

    today = date.today()
    latest_courses = Course.objects.filter(end_date__gte=today).order_by('-end_date')[:5]
    ctx = {"title":"Home", "events_list": Event.objects.all(), "courses_list": Course.objects.all(), "latest_events": Event.objects.order_by('date')[:5], "latest_courses": latest_courses}
    return render(request, template_name="index.html", context=ctx)

def go_control_panel (request): 
    return render(request, template_name="control_panel.html")