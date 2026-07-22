# web-interface Specification

## Purpose
Define the server-rendered URL interface for browsing movies, viewing details,
searching titles, and creating or updating authenticated reviews.
## Requirements
### Requirement: Home page

The application SHALL expose a home page at `/` that returns HTTP 200 and
renders links into the movie-browsing interface together with recently added
movies.

#### Scenario: Visit the home page

- **WHEN** a user sends `GET /`
- **THEN** the application renders the home template with up to five recently created movies

### Requirement: Browse and search movies

The application SHALL expose `/movies/` as a movie-list page with a Django form
submitted by GET. The optional `q` value MUST be stripped, MUST NOT exceed 255
characters, and MUST filter titles case-insensitively when non-blank. Invalid
input MUST display errors and MUST NOT execute a title search.

#### Scenario: Browse all movies

- **WHEN** a user sends `GET /movies/` without a query
- **THEN** the application returns HTTP 200 with all movies in model ordering and an unbound-looking search form

#### Scenario: Search by partial title

- **WHEN** a user sends `GET /movies/?q=spirit`
- **THEN** the application returns HTTP 200 with movies whose titles contain `spirit` regardless of case

#### Scenario: Reject an oversized search

- **WHEN** a user submits a `q` value longer than 255 characters
- **THEN** the application returns HTTP 200 with a form error and no movie results

#### Scenario: Reject a non-GET search request

- **WHEN** a client sends POST to `/movies/`
- **THEN** the application returns HTTP 405 without processing search input

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
users through a Django form. GET MUST render rating and body fields, valid POST
MUST accept a rating from 1 through 5 and non-blank review text, persist through
the review service, and redirect to movie detail. Invalid POST MUST preserve
submitted values, display field errors, and MUST NOT write a review.

#### Scenario: Anonymous user opens the review form

- **WHEN** an unauthenticated user requests the review form
- **THEN** the application redirects to the login page with a return URL

#### Scenario: Authenticated user submits a valid review

- **WHEN** an authenticated user posts a rating from 1 through 5 and a non-empty body
- **THEN** the application stores the user's review and redirects to the movie detail URL

#### Scenario: Authenticated user submits an invalid review

- **WHEN** an authenticated user posts an out-of-range rating or whitespace-only body
- **THEN** the application returns HTTP 200 with validation errors and does not store the invalid review

### Requirement: Documented URL API

Project documentation MUST list each application URL with its callable view,
HTTP method, accepted path/query/form arguments, successful response, redirect
behavior, and relevant error response.

#### Scenario: Developer checks the interface contract

- **WHEN** a developer reads the project documentation
- **THEN** they can determine how to call every basic application view and what each call returns

### Requirement: Register a user account

The application SHALL expose `/accounts/register/` as a registration form.
GET MUST render username, required email, password, and password-confirmation
fields. Valid POST MUST create and sign in the user before redirecting home.
Invalid POST MUST redisplay submitted non-password values and validation errors
without creating a user.

#### Scenario: Register with valid input

- **WHEN** an anonymous visitor submits a unique username, valid email, and matching policy-compliant passwords
- **THEN** the application creates and signs in the user and redirects to the home page

#### Scenario: Reject invalid registration input

- **WHEN** a visitor submits a duplicate username, invalid email, or invalid password confirmation
- **THEN** the application returns HTTP 200 with field errors and does not create a user
