## Homework 2

Building RESTful Movie Theater Booking Application using Python and Django.

Live Website: https://book-movie-seats-sahana.onrender.com/
(May take time to load. Your patience is appreciated!)

## Environment Setup

Create and activate a virtual environment:
python -m venv your_custom_env_name_here --system -site -packages
source your_custom_env_name_here/bin/activate

Install required dependencies:
Run 'pip install -r requirements.txt'

There are 59 tests in total (unit + integration + Behavior-Driven-Design). To run the tests, make sure the current directory is ~/cs5300/homework2/ and simply run 'python -m pytest'.

To run the app, make sure the current directory is ~/cs5300/homework2/ and run 'python manage.py runserver 0.0.0.0:3000'

## Application Design:
When users visit the website, they can browse the movies currently listed. They can also access My Bookings to view their own booking history or use Login to sign in. Clicking on a movie takes the user to the seat selection page, where they can choose a seat if they are logged in and the seat is still available. If a user is not logged in and tries to book, they can't select and book a seat. They have to log in first. From the login page, users can either log in with an existing account or register for a new one. After logging in, users can book an available seat for a movie and later view that reservation in the My Bookings page. Users can only view and manage their own bookings. If a booking is cancelled, that seat becomes available again for that specific movie. A seat that is booked for one movie may still be available for a different movie, as bookings are tied to the selected movie.

Relevant Files:
* models.py: Database models (Movie, Seat, Booking) are defined.
* views.py: Contains API viewsets and template views to render webpages.
* serializers.py: converts Movie,Seat and Booking objects to JSON so they can be returned by the REST API.
* forms.py: Registration form for new users.
* test_unit: Unit Tests
* test_integration: Integration tests (end to end)
* test_bdd: Behavior-Driven-Design tests (Also see booking_history.feature, movies.feature, seat_booking.feature udner bookings/features for gherkin scenarios).
* conftest.py: shared pytest fixtures that's used across all three test files (creates test users, movies, etc). This reduces redundancy as we don't have to recreate them for every test file.

## Acknowledgement: 
AI (ChatGPT and Claude) was used to generate a few integration tests and a few BDD scenarios.




