import datetime
import pytest
from bookings.models import Movie, Booking, Seat
from django.db import IntegrityError

"""
Testing Movie Model by creating an entry (Dune) and checking if it's been created correctly
"""
@pytest.mark.django_db
class TestMovieModel:
    def test_str_returns_title(self, movie):
        assert str(movie) == "Test Movie"

    def test_fields_stored_correctly(self, db):
        m = Movie.objects.create(
            title="Dune",
            description="Timothee and Zendaya.",
            release_date=datetime.date(2021, 10, 22),
            duration=155,
        )
        assert m.title == "Dune"
        assert m.description == "Timothee and Zendaya."
        assert m.release_date == datetime.date(2021, 10, 22)
        assert m.duration == 155

"""
Testing Seat Model including edge cases like trying to book a seat that's already booked for the movie. 
Also, trying to book the same seat (that's been booked for a movie) for another movie.
"""
@pytest.mark.django_db
class TestSeatModel:
    def test_str_returns_seat_number(self, seat):
        assert str(seat) == "A1"

    def test_is_available_for_unbooked_seat(self, seat, movie):
        assert seat.is_available_for(movie) is True

    def test_is_available_for_booked_seat(self, booking, seat, movie):
        assert seat.is_available_for(movie) is False

    def test_seat_booked_for_one_movie_is_free_for_another(self, booking, seat, movie2):
        assert seat.is_available_for(movie2) is True

"""
Testing Booking model including edge cases like the seat is still available for other movies.
User can only see their own booking.
"""
@pytest.mark.django_db
class TestBookingModel:
    def test_str_representation(self, booking):
        assert str(booking) == "sahana - Test Movie - A1"

    def test_unique_seat_per_movie_constraint(self, booking, other_user):
        with pytest.raises(IntegrityError):
            Booking.objects.create(
                movie=booking.movie,
                seat=booking.seat,
                user=other_user,
            )

    def test_same_seat_allowed_for_different_movies(self, seat, movie, movie2, user):
        Booking.objects.create(movie=movie, seat=seat, user=user)
        Booking.objects.create(movie=movie2, seat=seat, user=user)
        assert Booking.objects.count() == 2


    def test_user_only_sees_own_bookings(self, booking, other_user, movie, seat2):
        Booking.objects.create(movie=movie, seat=seat2, user=other_user)
        assert Booking.objects.filter(user=booking.user).count() == 1
        assert Booking.objects.filter(user=other_user).count() == 1
