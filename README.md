### README

This README provides instructions on how to set up your Django project, load songs from a CSV file into the database, update the search vectors, run the required migrations, and configure the search API.

#### Prerequisites

- Python 3.x
- Django
- PostgreSQL
- psycopg2-binary
- djangorestframework

#### 0. Start docker-compose

1. **Start the docker-compose to run the PostgreSQL database:**

    ```sh
    docker-compose up
    ```
2. Enter the container to run the migrations and load the songs from the CSV file:

    ```sh
    docker exec -it bude_server bash
    ```

#### 1. Run the Migrations

1. **Run the migrations to create the necessary database tables:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

#### 2. Load Songs from CSV

1. **Place your CSV file (`spotify_songs.csv`) in the project directory.**

2. **Run the management command to load the songs from the CSV file:**

    ```sh
    python manage.py load_songs
    ```

#### 3. Update Search Vector

1. **Run the management command to update the search vectors for the songs:**

    ```sh
    python manage.py update_search_vector
    ```


#### 4. Configure Search API

The search API provides two endpoints for searching songs in the database:

1. **Postgres Search API** (`/postgres-search/`): This endpoint uses PostgreSQL full-text search to return ranked search results based on the query. The API accepts two query parameters: `query` for the search term and `k` for the number of results to return.

2. **Custom Search API** (`/custom-search/`): This endpoint also uses PostgreSQL full-text search and provides a similar functionality to the Postgres Search API. It also accepts `query` for the search term and `k` for the number of results to return.

**API Usage Example:**

- **Postgres Search API:**

    ```
    GET /postgres-search/?query=your_search_term&k=10
    ```

- **Custom Search API:**

    ```
    GET /custom-search/?query=your_search_term&k=10
    ```

Both endpoints return a list of songs with the following fields:

- `track_id`: The unique ID of the track.
- `track_name`: The name of the track.
- `track_artist`: The artist of the track.
- `lyrics`: The lyrics of the track.
- `rank`: The relevance rank of the track based on the search query.

With these steps, you can set up your Django project, load song data, update the search vectors, and utilize the search API to perform efficient searches.