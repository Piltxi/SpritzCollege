from django.shortcuts import render
from Activities.models import Event

def go_home (request):

    ctx = {"title":"Home", "object_list": Event.objects.all()}
    return render(request, template_name="index.html", context=ctx)

