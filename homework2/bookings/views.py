from rest_framework import viewsets
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Seat, Booking
from collections import defaultdict
import re
from django.contrib import messages
from django.contrib.auth import login
from bookings.forms import RegisterForm

def register_page(request):
    if request.user.is_authenticated:
        return redirect("movie_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            return redirect("movie_list")
    else:
        form = RegisterForm()
    return render(request, "bookings/register.html", {"form": form})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def movie_list_page(request):
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})



@login_required
def seat_booking_page(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Handle booking POST
    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        seat = get_object_or_404(Seat, id=seat_id)

        if seat.is_booked:
            messages.error(request, f"Seat {seat.seat_number} is already booked.")
            return redirect("book_seat", movie_id=movie.id)

        # Create booking + mark seat booked
        Booking.objects.create(movie=movie, seat=seat, user=request.user)
        seat.is_booked = True
        seat.save()

        messages.success(request, f"Booked {seat.seat_number} for {movie.title}!")
        return redirect("booking_history")

    # GET: show layout
    seats = Seat.objects.all()

    rows = defaultdict(list)
    seat_re = re.compile(r"^([A-Za-z]+)\s*([0-9]+)$")

    for s in seats:
        m = seat_re.match(s.seat_number.strip())
        if m:
            row_letter = m.group(1).upper()
            seat_num = int(m.group(2))
        else:
            row_letter = "?"
            seat_num = 9999
        rows[row_letter].append((seat_num, s))

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