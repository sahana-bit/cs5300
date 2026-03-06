Feature: Seat Booking
  As a registered user
  I want to book a seat for a movie
  So that I can reserve my spot

  Background:
    Given the movie "Interstellar" exists with duration 169 minutes
    And seat "B3" exists

  Scenario: Guest sees seat page but cannot book without logging in
    When I visit the seat booking page for "Interstellar"
    Then the response status is 200
    And I see "log in" on the page

  Scenario: Guest posting a booking is redirected to login
    When an unauthenticated user tries to book seat "B3" for "Interstellar"
    Then I am redirected to the login page
    And no booking is created

  Scenario: Logged-in user can book a seat
    Given I am logged in as "sahana"
    When I book seat "B3" for "Interstellar"
    Then I am redirected back to the seat page
    And the booking exists in the database for "sahana"

  Scenario: A seat cannot be double-booked for the same movie
    Given "bob" has already booked seat "B3" for "Interstellar"
    And I am logged in as "sahana"
    When I book seat "B3" for "Interstellar"
    Then only 1 booking exists for "Interstellar"

  Scenario: Seat availability API is public
    When I request the seat list from the API
    Then the response status is 200
    And I see seat "B3" in the API response
