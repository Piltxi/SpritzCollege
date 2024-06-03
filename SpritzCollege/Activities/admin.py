from django.contrib import admin
from .models import Event, Booking, Course, Subscription

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'duration', 'price', 'max_capacity', 'place', 'status')
    search_fields = ('name', 'description', 'place')
    list_filter = ('status', 'date')
    ordering = ['date']

class BookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'num_seats', 'booking_time')
    search_fields = ('user__username', 'event__name')
    list_filter = ('booking_time',)
    ordering = ['event', 'user']

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'recurrence_day', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category', 'start_date')
    ordering = ['start_date']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'subscription_date')
    search_fields = ('user__username', 'course__name')
    list_filter = ('subscription_date',)
    ordering = ['subscription_date']

admin.site.register(Event, EventAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
