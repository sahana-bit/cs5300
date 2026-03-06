Feature: Booking History
  As a registered user
  I want to view and manage my booking history
  So that I know which seats I have reserved

  Background:
    Given the movie "Insidious" exists with duration 136 minutes
    And seat "A1" exists

  Scenario: User sees their own bookings in history
    Given I am logged in as "sahana"
    And "sahana" has already booked seat "A1" for "Insidious"
    When I visit the booking history page
    Then the response status is 200
    And I see "Insidious" on the page
    And I see "A1" on the page

  Scenario: User does not see other users bookings
    Given I am logged in as "sahana"
    And "Jayden" has already booked seat "A1" for "Insidious"
    When I visit the booking history page
    Then I do not see "A1" on the page

  Scenario: Unauthenticated user is redirected from booking history
    When I visit the booking history page as a guest
    Then I am redirected to the login page

  Scenario: User can cancel their own booking
    Given I am logged in as "sahana"
    And "sahana" has already booked seat "A1" for "Insidious"
    When I cancel my booking for "Insidious" seat "A1"
    Then no booking exists for "sahana"
    And I am redirected back to the seat page

  Scenario: Booking API only shows the current users bookings
    Given I am logged in as "sahana"
    And "sahana" has already booked seat "A1" for "Insidious"
    And seat "A2" exists
    And "dave" has already booked seat "A2" for "Insidious"
    When I request my bookings from the API
    Then the response status is 200
    And the response contains 1 booking
