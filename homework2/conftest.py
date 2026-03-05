import datetime
import pytest


@pytest.fixture
def movie(db):
    from bookings.models import Movie
    return Movie.objects.create(
        title="Test Movie",
        description="A great film.",
        release_date=datetime.date(2024, 1, 1),
        duration=120,
    )

@pytest.fixture
def movie2(db):
    from bookings.models import Movie
    return Movie.objects.create(
        title="Second Movie",
        description="Another film.",
        release_date=datetime.date(2024, 6, 1),
        duration=90,
    )

@pytest.fixture
def seat(db):
    from bookings.models import Seat
    return Seat.objects.create(seat_number="A1")

@pytest.fixture
def seat2(db):
    from bookings.models import Seat
    return Seat.objects.create(seat_number="A2")

@pytest.fixture
def user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(username="testuser", password="testpass123")

@pytest.fixture
def other_user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(username="otheruser", password="testpass123")

@pytest.fixture
def admin_user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(username="admin", password="testpass123", is_staff=True)

@pytest.fixture
def booking(db, movie, seat, user):
    from bookings.models import Booking
    return Booking.objects.create(movie=movie, seat=seat, user=user)

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def browser_client(client, user):
    client.force_login(user)
    return client
