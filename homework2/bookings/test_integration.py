"""
Integration Tests — REST API endpoints and template views end-to-end.
Run with:  pytest bookings/test_integration.py -v
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMovieAPI:

    def test_list_movies_returns_correct_data(self, api_client, movie):
        r = api_client.get("/api/movies/")
        titles = [m["title"] for m in r.json()]
        assert "Test Movie" in titles

    def test_retrieve_single_movie(self, api_client, movie):
        r = api_client.get(f"/api/movies/{movie.id}/")
        assert r.status_code == status.HTTP_200_OK
        assert r.json()["title"] == "Test Movie"

    def test_retrieve_nonexistent_movie_returns_404(self, api_client):
        r = api_client.get("/api/movies/Conjuring/")
        assert r.status_code == status.HTTP_404_NOT_FOUND

    def test_create_movie_as_admin_returns_201(self, admin_client):
        from bookings.models import Movie
        payload = {"title": "New Film", "description": "Desc", "release_date": "2024-06-01", "duration": 100}
        r = admin_client.post("/api/movies/", payload)
        assert r.status_code == status.HTTP_201_CREATED
        assert Movie.objects.filter(title="New Film").exists()

    def test_create_movie_as_regular_user_returns_403(self, auth_client):
        payload = {"title": "Blocked", "description": "Desc", "release_date": "2024-06-01", "duration": 90}
        r = auth_client.post("/api/movies/", payload)
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_create_movie_unauthenticated_returns_403(self, api_client):
        payload = {"title": "Blocked", "description": "Desc", "release_date": "2024-06-01", "duration": 90}
        r = api_client.post("/api/movies/", payload)
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_update_movie_as_admin(self, admin_client, movie):
        r = admin_client.patch(f"/api/movies/{movie.id}/", {"title": "Updated"})
        assert r.status_code == status.HTTP_200_OK
        movie.refresh_from_db()
        assert movie.title == "Updated"

    def test_delete_movie_as_admin(self, admin_client, movie):
        from bookings.models import Movie
        r = admin_client.delete(f"/api/movies/{movie.id}/")
        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert Movie.objects.count() == 0


@pytest.mark.django_db
class TestSeatAPI:

    def test_list_seats_unauthenticated_returns_200(self, api_client, seat):
        r = api_client.get("/api/seats/")
        assert r.status_code == status.HTTP_200_OK

    def test_list_seats_returns_correct_data(self, api_client, seat):
        r = api_client.get("/api/seats/")
        numbers = [s["seat_number"] for s in r.json()]
        assert "A1" in numbers

    def test_create_seat_as_admin(self, admin_client):
        r = admin_client.post("/api/seats/", {"seat_number": "C3"})
        assert r.status_code == status.HTTP_201_CREATED

    def test_create_seat_as_regular_user_returns_403(self, auth_client):
        r = auth_client.post("/api/seats/", {"seat_number": "C3"})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_seat_as_admin(self, admin_client, seat):
        from bookings.models import Seat
        r = admin_client.delete(f"/api/seats/{seat.id}/")
        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert Seat.objects.count() == 0


@pytest.mark.django_db
class TestBookingAPI:

    def test_list_bookings_unauthenticated_returns_403(self, api_client):
        r = api_client.get("/api/bookings/")
        assert r.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_list_bookings_returns_only_own(self, auth_client, booking, other_user, movie, seat2):
        from bookings.models import Booking
        Booking.objects.create(movie=movie, seat=seat2, user=other_user)
        r = auth_client.get("/api/bookings/")
        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 1

    def test_create_booking_authenticated(self, auth_client, movie, seat):
        from bookings.models import Booking
        r = auth_client.post("/api/bookings/", {"movie": movie.id, "seat": seat.id})
        assert r.status_code == status.HTTP_201_CREATED
        assert Booking.objects.count() == 1


    def test_create_duplicate_booking_returns_400(self, auth_client, booking, movie, seat):
        r = auth_client.post("/api/bookings/", {"movie": movie.id, "seat": seat.id})
        assert r.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.django_db
class TestMovieListView:

    def test_returns_200(self, client):
        r = client.get(reverse("movie_list"))
        assert r.status_code == 200

    def test_shows_movie_titles(self, client, movie):
        r = client.get(reverse("movie_list"))
        assert b"Test Movie" in r.content

    def test_empty_state_message(self, client):
        r = client.get(reverse("movie_list"))
        assert b"No movies yet" in r.content


@pytest.mark.django_db
class TestSeatBookingView:

    def test_returns_200(self, client, movie):
        r = client.get(reverse("book_seat", args=[movie.id]))
        assert r.status_code == 200


    def test_shows_movie_title(self, client, movie):
        r = client.get(reverse("book_seat", args=[movie.id]))
        assert b"Test Movie" in r.content

    def test_shows_seats(self, client, movie, seat):
        r = client.get(reverse("book_seat", args=[movie.id]))
        assert b"A1" in r.content

    def test_404_for_nonexistent_movie(self, client):
        r = client.get(reverse("book_seat", args=[9999]))
        assert r.status_code == 404

    def test_guest_sees_login_warning(self, client, movie):
        r = client.get(reverse("book_seat", args=[movie.id]))
        assert b"log in" in r.content.lower()

    def test_booking_as_logged_in_user(self, browser_client, movie, seat):
        from bookings.models import Booking
        r = browser_client.post(reverse("book_seat", args=[movie.id]), {"seat_id": seat.id})
        assert r.status_code == 302
        assert Booking.objects.count() == 1

    def test_booking_taken_seat_blocked(self, browser_client, booking, movie, seat):
        from bookings.models import Booking
        browser_client.post(reverse("book_seat", args=[movie.id]), {"seat_id": seat.id})
        assert Booking.objects.count() == 1



@pytest.mark.django_db
class TestBookingHistoryView:

    def test_unauthenticated_redirects(self, client):
        r = client.get(reverse("booking_history"))
        assert r.status_code == 302
        assert "/accounts/login/" in r["Location"]

    def test_authenticated_returns_200(self, browser_client):
        r = browser_client.get(reverse("booking_history"))
        assert r.status_code == 200


    def test_shows_own_bookings(self, browser_client, booking):
        r = browser_client.get(reverse("booking_history"))
        assert b"Test Movie" in r.content
        assert b"A1" in r.content

    def test_does_not_show_other_users_bookings(self, browser_client, other_user, movie, seat2):
        from bookings.models import Booking
        Booking.objects.create(movie=movie, seat=seat2, user=other_user)
        r = browser_client.get(reverse("booking_history"))
        assert b"A2" not in r.content


@pytest.mark.django_db
class TestCancelBookingView:

    def test_cancel_own_booking_deletes_it(self, browser_client, booking):
        from bookings.models import Booking
        browser_client.post(reverse("cancel_booking", args=[booking.id]))
        assert Booking.objects.count() == 0

    def test_cancel_redirects_to_seat_page(self, browser_client, booking):
        r = browser_client.post(reverse("cancel_booking", args=[booking.id]))
        assert r.status_code == 302

    def test_cannot_cancel_other_users_booking(self, browser_client, other_user, movie, seat2):
        from bookings.models import Booking
        other_booking = Booking.objects.create(movie=movie, seat=seat2, user=other_user)
        r = browser_client.post(reverse("cancel_booking", args=[other_booking.id]))
        assert r.status_code == 404
        assert Booking.objects.count() == 1

    def test_cancel_requires_post_not_get(self, browser_client, booking):
        r = browser_client.get(reverse("cancel_booking", args=[booking.id]))
        assert r.status_code == 405

    def test_unauthenticated_cancel_redirects_to_login(self, client, booking):
        r = client.post(reverse("cancel_booking", args=[booking.id]))
        assert r.status_code == 302
        assert "/accounts/login/" in r["Location"]
