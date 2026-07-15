## ADDED Requirements

### Requirement: Runnable Django domain application

The project SHALL include a generated `reviews` Django application, register
that application in project settings, and provide migrations that create its
schema in the configured SQLite database.

#### Scenario: Fresh database setup

- **WHEN** a developer applies migrations to an empty development database
- **THEN** Django creates the built-in tables and all Film Reviews domain tables without system-check errors

### Requirement: Movie persistence

The system SHALL persist each movie with a title, optional release date,
optional synopsis, and creation and update timestamps. Movie titles MUST be
indexed but MUST NOT be required to be unique.

#### Scenario: Store movies with the same title

- **WHEN** two distinct movies have the same title
- **THEN** both movie records can be stored and distinguished by their identifiers and other metadata

### Requirement: User-authored review persistence

The system SHALL associate every review with exactly one configured Django
user and exactly one movie. Deleting either related record SHALL delete its
reviews.

#### Scenario: Access related reviews

- **WHEN** a review is stored for a user and movie
- **THEN** the review is accessible through both the user's and the movie's `reviews` relationship

#### Scenario: Delete a reviewed movie

- **WHEN** a movie is deleted
- **THEN** all reviews for that movie are deleted by the database relationship

### Requirement: Rating integrity

Every review rating MUST be an integer from 1 through 5 inclusive. The system
SHALL enforce the range through Django validation and a database check
constraint.

#### Scenario: Accept a boundary rating

- **WHEN** a review is validated with a rating of 1 or 5
- **THEN** rating validation succeeds

#### Scenario: Reject an out-of-range rating

- **WHEN** a review rating below 1 or above 5 is validated or written directly to the database
- **THEN** the operation fails without storing the invalid rating

### Requirement: One review per user and movie

The system MUST allow at most one review by a given user for a given movie.

#### Scenario: Reject a duplicate review

- **WHEN** a user who already reviewed a movie attempts to store another review for that movie
- **THEN** the database rejects the duplicate while allowing other users to review the same movie

### Requirement: Current average rating

The system SHALL calculate a movie's average rating from its current related
reviews and SHALL NOT persist a duplicated average on the movie record. An
unrated movie SHALL return no average.

#### Scenario: Average current reviews

- **WHEN** a movie has ratings of 3 and 5
- **THEN** the rating service returns an average of 4.0

#### Scenario: Report an unrated movie

- **WHEN** a movie has no reviews
- **THEN** the rating service returns `None`

### Requirement: Human-readable admin labels

Movie and review records MUST implement meaningful string representations and
SHALL be registered in Django admin.

#### Scenario: Identify records in admin

- **WHEN** an administrator views movie or review choices and lists
- **THEN** movies display their title and optional release year, and reviews display their author, movie, and rating
