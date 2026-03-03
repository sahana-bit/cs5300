from django.contrib import admin
from .models import Movie, Seat, Showtime, Booking

admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Showtime)
admin.site.register(Booking)