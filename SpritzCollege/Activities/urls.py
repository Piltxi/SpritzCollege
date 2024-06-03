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
from django.urls import path

from .views import *

urlpatterns = [
    
    #* public views
    path('calendar/', calendar_spritzcollege_view, name='calendar_view'),
    path("events/", EventsList.as_view(), name="list_events"),
    path("courses/", CoursesList.as_view(), name="list_courses"),
    
    #* EVENTS
    path('events/detail/<int:pk>/', EventDetail.as_view(), name='event_detail'), 
    path("events/new/", AddEvents.as_view(),name="new_event"),
    path('events/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('export/active-events/', ExportActiveEventsToExcelView.as_view(), name='export_active_events_to_excel'),
    
    #* COURSES
    path('courses/detail/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
    path("courses/new/", AddCourse.as_view(),name="new_course"),
    path('courses/update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses/<int:course_id>/pdf/', course_brochure_pdf, name='course_brochure_pdf'),

    #* BOOKING user personal urls
    path('events/newbooking/<int:event_id>/', book_event, name='event_newbooking'),
    
    path('events/my-bookings/', UserBookingListView.as_view(), name='user_event_booking_list'),
    path('events/my-bookings/update/<int:pk>/', UserBookingUpdateView.as_view(), name='user_event_booking_update'),
    path('events/my-bookings/delete/<int:pk>/', UserBookingDeleteView.as_view(), name='user_event_booking_delete'),
    path('activities/booking/<int:booking_id>/pdf/', generate_booking_pdf, name='user_booking_pdf'),
    
    path('my-calendar/', calendar_user_view, name='user_calendar'),
    
    #* BOOKING ADMIN personal urls
    path('events/booking/<int:evento_id>', AdminEventBookingsView.as_view(), name='bookings_view'),
    path('events/booking/adm/<int:pk>/update/', AdminBookingUpdateView.as_view(), name='admin_event_booking_update'),
    path('events/booking/adm/<int:pk>/delete/', AdminBookingDeleteView.as_view(), name='admin_booking_delete'),
    
    #* SUBSCRIBES user urls
    path('subscriptions/', UserSubscriptionListView.as_view(), name='subscription_list'),
    path('subscriptions/new/<int:course_id>/', subscribe_to_course, name='new_subscription'),
    path('subscriptions/<int:pk>/delete/', UserSubscriptionDeleteView.as_view(), name='subscription_delete'),
    
    #* SUBSCRIBES ADMIN urls
    path('courses/<int:course_id>/subscriptions/', CourseSubscriptionListView.as_view(), name='course_subscriptions'),
    path('course/<int:course_id>/subscriptions/export/', ExportCourseSubscriptionsExcelView.as_view(), name='export_course_subscriptions_excel'),
    path('subscriptions/booking/adm/<int:pk>/delete/', AdminUserSubscriptionDeleteView.as_view(), name='admin_sub_delete'),
    
]

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
