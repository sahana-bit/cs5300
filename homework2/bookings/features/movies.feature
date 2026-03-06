Feature: Movie Listings
  As a visitor
  I want to browse available movies
  So that I can decide which one to book

  Background:
    Given the movie "Oppenheimer" exists with duration 180 minutes
    And the movie "Barbie" exists with duration 114 minutes

  Scenario: Visitor sees all movies on the listing page
    When I visit the movie list page
    Then the response status is 200
    And I see "Oppenheimer" on the page
    And I see "Barbie" on the page

  Scenario: The movie list API is public
    When I request the movie list from the API as an unauthenticated user
    Then the response status is 200


  Scenario: Admin can create a movie via the API
    Given I am logged in as an admin
    When I create a movie "Dune" via the API with duration 155 minutes
    Then the response status is 201
    And "Dune" exists in the database
