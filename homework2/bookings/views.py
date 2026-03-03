from rest_framework import viewsets
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Seat, Booking
from collections import defaultdict
import re

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def movie_list_page(request):
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})



@login_required
def seat_booking_page(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    seats = Seat.objects.all()

    # Group like A1, A2 -> row "A"; B1.. -> row "B"
    rows = defaultdict(list)
    seat_re = re.compile(r"^([A-Za-z]+)\s*([0-9]+)$")

    for s in seats:
        m = seat_re.match(s.seat_number.strip())
        if m:
            row_letter = m.group(1).upper()
            seat_num = int(m.group(2))
        else:
            # fallback (if formatting is weird)
            row_letter = "?"
            seat_num = 9999

        rows[row_letter].append((seat_num, s))

    # Sort rows alphabetically, and seats numerically inside each row
    seat_rows = []
    for row_letter in sorted(rows.keys()):
        seat_rows.append((row_letter, [s for _, s in sorted(rows[row_letter], key=lambda x: x[0])]))

    return render(request, "bookings/seat_booking.html", {
        "movie": movie,
        "seat_rows": seat_rows,
    })

@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat").order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})