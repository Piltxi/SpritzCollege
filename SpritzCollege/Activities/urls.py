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
    
    #* public views
    path('calendar/', calendar_view, name='calendar_view'),
    path("events/", EventsList.as_view(), name="list_events"),
    path("courses/", CoursesList.as_view(), name="list_courses"),
    path("about-as/", aboutAs_view, name="about_us"),
    
    #* EVENTS
    path('events/detail/<int:pk>/', EventDetail.as_view(), name='event_detail'), 
    path("events/new/", AddEvents.as_view(),name="new_event"),
    path('events/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    
    #* COURSES
    path('courses/detail/<int:pk>/', CourseDetail.as_view(), name='course_detail'),  # Cambia course_id in pk 
    path("courses/new/", AddCourse.as_view(),name="new_course"),
    path('courses/update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses/<int:course_id>/pdf/', course_pdf, name='course_pdf'),

    #* BOOKING user personal urls
    path('events/newbooking/<int:event_id>/', book_event, name='event_newbooking'),
    
    path('events/my-bookings/', UserBookingListView.as_view(), name='user_event_booking_list'),
    path('events/my-bookings/update/<int:pk>/', UserBookingUpdateView.as_view(), name='user_event_booking_update'),
    path('events/my-bookings/delete/<int:pk>/', UserBookingDeleteView.as_view(), name='user_event_booking_delete'),
    
    # booking admin urls
    path('events/booking/<int:evento_id>', EventBookingsView.as_view(), name='bookings_view'),
    path('events/booking/adm/<int:pk>/update/', AdminBookingUpdateView.as_view(), name='admin_event_booking_update'),
    path('events/booking/adm/<int:pk>/delete/', AdminBookingDeleteView.as_view(), name='admin_booking_delete'),
    
    #* SUBSCRIBES user personal urls
    path('subscriptions/new/<int:course_id>/', SubscriptionCreateView.as_view(), name='new_subscription'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
    path('subscriptions/<int:pk>/edit/', SubscriptionUpdateView.as_view(), name='subscription_update'),
    path('subscriptions/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    
    path('courses/<int:course_id>/subscriptions/', CourseSubscriptionListView.as_view(), name='course_subscriptions'),
]

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
