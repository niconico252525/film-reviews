## ADDED Requirements

### Requirement: Home page

The application SHALL expose a home page at `/` that returns HTTP 200 and
renders links into the movie-browsing interface together with recently added
movies.

#### Scenario: Visit the home page

- **WHEN** a user sends `GET /`
- **THEN** the application renders the home template with up to five recently created movies

### Requirement: Browse and search movies

The application SHALL expose `/movies/` as a movie-list page. It MUST accept an
optional `q` query argument and filter titles case-insensitively when the
argument is non-blank.

#### Scenario: Browse all movies

- **WHEN** a user sends `GET /movies/` without a query
- **THEN** the application returns HTTP 200 with all movies in model ordering

#### Scenario: Search by partial title

- **WHEN** a user sends `GET /movies/?q=spirit`
- **THEN** the application returns HTTP 200 with movies whose titles contain `spirit` regardless of case

### Requirement: View movie details

The application SHALL expose `/movies/<movie_id>/` and render the selected
movie, its current average rating, and its reviews.

#### Scenario: View an existing movie

- **WHEN** a user requests the detail URL for an existing movie identifier
- **THEN** the application returns HTTP 200 with the movie, average rating, and related reviews

#### Scenario: Request an unknown movie

- **WHEN** a user requests the detail URL for an unknown movie identifier
- **THEN** the application returns HTTP 404

### Requirement: Submit or update a review

The application SHALL expose `/movies/<movie_id>/reviews/new/` to authenticated
users. GET MUST render a rating/body form, valid POST MUST create or update that
user's review and redirect to movie detail, and invalid POST MUST redisplay the
form without writing a review.

#### Scenario: Anonymous user opens the review form

- **WHEN** an unauthenticated user requests the review form
- **THEN** the application redirects to the login page with a return URL

#### Scenario: Authenticated user submits a valid review

- **WHEN** an authenticated user posts a rating from 1 through 5 and a non-empty body
- **THEN** the application stores the user's review and redirects to the movie detail URL

#### Scenario: Authenticated user submits an invalid review

- **WHEN** an authenticated user posts an out-of-range rating or empty body
- **THEN** the application returns HTTP 200 with validation errors and does not store the invalid review

### Requirement: Documented URL API

Project documentation MUST list each application URL with its callable view,
HTTP method, accepted path/query/form arguments, successful response, redirect
behavior, and relevant error response.

#### Scenario: Developer checks the interface contract

- **WHEN** a developer reads the project documentation
- **THEN** they can determine how to call every basic application view and what each call returns
