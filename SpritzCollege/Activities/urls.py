"""
URL configuration for SpritzCollege project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from .views import *

urlpatterns = [
    
    path("events/", EventsList.as_view(), name="list_events"),
    path("courses/", CoursesList.as_view(), name="list_courses"),
    
    # path('event/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    # path('event/<int:event_id>/', event_detail, name='event_detail'),
    
    path('event/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('course/<int:course_id>/', EventDetail.as_view, name='course_detail'),
    
    path("new/event/", AddEvents.as_view(),name="new_event"),
    path("new/course/", AddCourse.as_view(),name="new_course"),
    
    path('booking/<int:event_id>/', book_event, name='booking'),

    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('my-bookings/', MyBookingsListView.as_view(), name='my_bookings'),
    path('cancel_booking/<int:pk>/', MyBookingDeleteView.as_view(), name='cancel_booking'),
    path('booking/<int:pk>/update/', MyBookingUpdateView.as_view(), name='booking_update'),

    path('booking/<int:pk>/delete/', AdminBookingDeleteView.as_view(), name='admin_booking_delete'),
    path('booking/<int:pk>/update/', AdminBookingUpdateView.as_view(), name='admin_booking_update'),

    path('eventi/<int:evento_id>/prenotazioni/', PrenotazioniEventoView.as_view(), name='prenotazioni_evento'),
    # path("ricerca/", search, name="cercalibro"),
    # path("ricerca/<str:sstring>/<str:where>/", LibroRicercaView.as_view(), name="ricerca_risultati")
]

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
