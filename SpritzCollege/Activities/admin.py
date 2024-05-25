from django.contrib import admin

from .models import Event, Course, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'place', 'status', 'max_capacity', 'price')
    search_fields = ('name', 'description', 'place')
    list_filter = ('status', 'date')
    ordering = ('date',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'recurrence_day', 'category')
    search_fields = ('name', 'description', 'category')
    list_filter = ('category', 'start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'num_seats', 'booking_time')
    search_fields = ('user__username', 'event__name')
    list_filter = ('event', 'booking_time')
    ordering = ('-booking_time',)
