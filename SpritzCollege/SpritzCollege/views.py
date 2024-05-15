from django.shortcuts import render
from Activities.models import Event, Course

def go_home (request):

    ctx = {"title":"Home", "events_list": Event.objects.all(), "courses_list": Course.objects.all()}
    return render(request, template_name="index.html", context=ctx)

def go_control_panel (request): 
    return render(request, template_name="control_panel.html")