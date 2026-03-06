import datetime
import pytest
from pytest_bdd import given, when, then, scenario, parsers
from bookings.models import Booking, Seat, Movie
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

"""
Scenario declarations. Each scenario in the .feature files has a function
"""
# movies
@scenario("features/movies.feature", "Visitor sees all movies on the listing page")
def test_visitor_sees_movies(): pass

@scenario("features/movies.feature", "The movie list API is public")
def test_movie_api_public(): pass

@scenario("features/movies.feature", "Admin can create a movie via the API")
def test_admin_creates_movie(): pass

# seat_booking
@scenario("features/seat_booking.feature", "Guest sees seat page but cannot book without logging in")
def test_guest_sees_seat_page(): pass

@scenario("features/seat_booking.feature", "Guest posting a booking is redirected to login")
def test_guest_post_redirects(): pass

@scenario("features/seat_booking.feature", "Logged-in user can book a seat")
def test_logged_in_user_books(): pass

@scenario("features/seat_booking.feature", "A seat cannot be double-booked for the same movie")
def test_no_double_booking(): pass

@scenario("features/seat_booking.feature", "Seat availability API is public")
def test_seat_api_public(): pass

# booking_history
@scenario("features/booking_history.feature", "User sees their own bookings in history")
def test_user_sees_own_history(): pass

@scenario("features/booking_history.feature", "User does not see other users bookings")
def test_user_cannot_see_others(): pass

@scenario("features/booking_history.feature", "Unauthenticated user is redirected from booking history")
def test_unauth_redirected_from_history(): pass

@scenario("features/booking_history.feature", "User can cancel their own booking")
def test_user_can_cancel(): pass

@scenario("features/booking_history.feature", "Booking API only shows the current users bookings")
def test_api_shows_own_bookings_only(): pass


"""
Functions for Given steps in the scenario
"""
@given(parsers.parse('the movie "{title}" exists with duration {duration:d} minutes'))
def movie_exists(db, title, duration):
    movie, _ = Movie.objects.get_or_create(
        title=title,
        defaults={
            "description": f"About {title}.",
            "release_date": datetime.date(2024, 1, 1),
            "duration": duration,
        },
    )
    return movie


@given(parsers.parse('seat "{seat_number}" exists'))
def seat_exists(db, seat_number):
    seat, _ = Seat.objects.get_or_create(seat_number=seat_number)
    return seat


@given(parsers.parse('I am logged in as "{username}"'), target_fixture="active_client")
def logged_in_as(db, client, username):
    user, _ = User.objects.get_or_create(username=username)
    user.set_password("pw")
    user.save()
    client.force_login(user)
    return client


@given("I am logged in as an admin", target_fixture="active_api_client")
def logged_in_as_admin(db):
    admin, _ = User.objects.get_or_create(username="bdd_admin", defaults={"is_staff": True})
    admin.is_staff = True
    admin.set_password("pw")
    admin.save()
    c = APIClient()
    c.force_authenticate(user=admin)
    return c


@given(parsers.parse('"{username}" has already booked seat "{seat_number}" for "{movie_title}"'))
def user_has_booked(db, username, seat_number, movie_title):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password("pw")
        user.save()
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    Booking.objects.get_or_create(movie=movie, seat=seat, defaults={"user": user})


"""
Functions for When steps in scenarios
"""
@when("I visit the movie list page", target_fixture="response")
def visit_movie_list(client):
    return client.get(reverse("movie_list"))


@when("I request the movie list from the API as an unauthenticated user", target_fixture="response")
def api_list_movies_unauth():
    return APIClient().get("/api/movies/")


@when(parsers.parse('I request the movie "{title}" from the API'), target_fixture="response")
def api_get_movie(title):
    movie = Movie.objects.get(title=title)
    return APIClient().get(f"/api/movies/{movie.id}/")


@when("an unauthenticated user tries to create a movie via the API", target_fixture="response")
def api_create_movie_unauth():
    return APIClient().post("/api/movies/", {
        "title": "Blocked", "description": "x",
        "release_date": "2024-01-01", "duration": 90,
    })


@when(parsers.parse('I create a movie "{title}" via the API with duration {duration:d} minutes'),
      target_fixture="response")
def api_create_movie(active_api_client, title, duration):
    return active_api_client.post("/api/movies/", {
        "title": title,
        "description": f"About {title}.",
        "release_date": "2024-01-01",
        "duration": duration,
    })


@when(parsers.parse('I visit the seat booking page for "{movie_title}"'), target_fixture="response")
def visit_seat_page(client, movie_title):
    movie = Movie.objects.get(title=movie_title)
    return client.get(reverse("book_seat", args=[movie.id]))


@when(parsers.parse('an unauthenticated user tries to book seat "{seat_number}" for "{movie_title}"'),
      target_fixture="response")
def guest_books_seat(client, seat_number, movie_title):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    return client.post(reverse("book_seat", args=[movie.id]), {"seat_id": seat.id})


@when(parsers.parse('I book seat "{seat_number}" for "{movie_title}"'), target_fixture="response")
def user_books_seat(active_client, seat_number, movie_title):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    return active_client.post(reverse("book_seat", args=[movie.id]), {"seat_id": seat.id})


@when("I request the seat list from the API", target_fixture="response")
def api_list_seats():
    return APIClient().get("/api/seats/")


@when("I visit the booking history page", target_fixture="response")
def visit_history(active_client):
    return active_client.get(reverse("booking_history"))


@when("I visit the booking history page as a guest", target_fixture="response")
def visit_history_guest(client):
    return client.get(reverse("booking_history"))


@when(parsers.parse('I cancel my booking for "{movie_title}" seat "{seat_number}"'),
      target_fixture="response")
def cancel_booking(active_client, movie_title, seat_number):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    # find the booking via the seat and movie when user is logged in
    booking = Booking.objects.get(movie=movie, seat=seat)
    return active_client.post(reverse("cancel_booking", args=[booking.id]))


@when("I request my bookings from the API", target_fixture="response")
def api_list_bookings(active_client):
    user = User.objects.get(username="sahana")
    c = APIClient()
    c.force_authenticate(user=user)
    return c.get("/api/bookings/")


"""
Functions for Then steps in scenarios
"""
@then(parsers.parse("the response status is {status_code:d}"))
def check_status(response, status_code):
    assert response.status_code == status_code, \
        f"Expected {status_code}, got {response.status_code}"


@then(parsers.parse('I see "{text}" on the page'))
def see_text(response, text):
    assert text.lower() in response.content.decode().lower(), \
        f"Expected '{text}' in page"


@then(parsers.parse('I do not see "{text}" on the page'))
def not_see_text(response, text):
    assert text.lower() not in response.content.decode().lower(), \
        f"Did not expect '{text}' in page"


@then(parsers.parse('the JSON field "{field}" equals "{value}"'))
def json_field_equals(response, field, value):
    data = response.json()
    assert str(data.get(field)) == value, \
        f"Expected JSON['{field}'] == '{value}', got '{data.get(field)}'"


@then(parsers.parse('"{title}" exists in the database'))
def movie_in_db(title):
    assert Movie.objects.filter(title=title).exists()


@then("I am redirected to the login page")
def redirected_to_login(response):
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@then("I am redirected back to the seat page")
def redirected_to_seat_page(response):
    assert response.status_code == 302


@then("no booking is created")
def no_booking_created():
    assert Booking.objects.count() == 0


@then(parsers.parse('the booking exists in the database for "{username}"'))
def booking_exists_for_user(username):
    user = User.objects.get(username=username)
    assert Booking.objects.filter(user=user).exists()


@then(parsers.parse('only {count:d} booking exists for "{movie_title}"'))
def only_n_bookings(count, movie_title):
    movie = Movie.objects.get(title=movie_title)
    assert Booking.objects.filter(movie=movie).count() == count


@then(parsers.parse('I see seat "{seat_number}" in the API response'))
def seat_in_api(response, seat_number):
    numbers = [s["seat_number"] for s in response.json()]
    assert seat_number in numbers


@then(parsers.parse('no booking exists for "{username}"'))
def no_booking_for_user(username):
    user = User.objects.get(username=username)
    assert not Booking.objects.filter(user=user).exists()


@then(parsers.parse("the response contains {count:d} booking"))
def response_contains_n_bookings(response, count):
    assert len(response.json()) == count
