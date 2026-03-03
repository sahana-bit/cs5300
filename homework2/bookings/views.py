import re
from rest_framework import viewsets
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer, ShowtimeSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .models import Seat, Showtime, Booking
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import login
from bookings.forms import RegisterForm
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.urls import reverse
from django.shortcuts import redirect

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:   # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff
    
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
    permission_classes = [IsAdminOrReadOnly]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAdminOrReadOnly]

def movie_list_page(request):
    movies = Movie.objects.prefetch_related("showtimes").all()
    return render(request, "bookings/movie_list.html", {"movies": movies})


def seat_booking_page(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = Seat.objects.all()

    # Seats already booked for THIS showtime
    booked_seat_ids = set(
        Booking.objects.filter(showtime=showtime).values_list("seat_id", flat=True)
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
           messages.warning(request, "Please log in to book a seat. We don't support non-users at this time.")
           return redirect(f"{reverse('login')}?next={request.path}")
        seat_id = int(request.POST.get("seat_id"))
        if seat_id in booked_seat_ids:
            messages.error(request, "That seat was just booked by someone else. Pick another.")
            return redirect("book_seat", showtime_id=showtime.id)

        try:
            Booking.objects.create(showtime=showtime, seat_id=seat_id, user=request.user)
            messages.success(request, "Seat booked!")
        except IntegrityError:
            # Handles race condition: two users click same seat at same time
            messages.error(request, "That seat was just booked by someone else. Pick another.")

        return redirect("book_seat", showtime_id=showtime.id)

    # Seat Map
    rows = defaultdict(list)
    seat_re = re.compile(r"^([A-Za-z]+)\s*([0-9]+)$")

    for s in seats:
        m = seat_re.match(s.seat_number.strip())
        row = m.group(1).upper() if m else "?"
        num = int(m.group(2)) if m else 9999
        rows[row].append((num, s))

    seat_rows = [(row, [s for _, s in sorted(items)]) for row, items in sorted(rows.items())]

    return render(request, "bookings/seat_booking.html", {
    "showtime": showtime,
    "seat_rows": seat_rows,
    "booked_seat_ids": booked_seat_ids,
    "can_book": request.user.is_authenticated,
})

@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).select_related("showtime__movie", "seat").order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


@require_POST
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    showtime_id = booking.showtime_id
    booking.delete()
    messages.success(request, "Booking cancelled. Seat is available again.")
    return redirect("book_seat", showtime_id=showtime_id)