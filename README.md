# BUDE Recommendation System

This README provides instructions on how to set up the Django project,
load songs from a CSV file into the database, update the search vectors, 
run the required migrations, and configure the search API.

### Setup

#### Prerequisites

- Python 3.x
- Django
- PostgreSQL
- psycopg2-binary
- djangorestframework

#### 0. Start Docker Compose

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

#### 4. Create Our Custom Inverted Index

1. **Run the management command to create the inverted index for the songs:**

    ```sh
    python manage.py build_index
    ```

#### 5. Configure Search API

The search API provides two endpoints for searching songs in the database:

1. **Postgres Search API** (`/postgres-search/`): This endpoint uses PostgreSQL full-text search to return ranked search results based on the query. The API accepts two query parameters: `query` for the search term and `k` for the number of results to return.

2. **Custom Search API** (`/custom-search/`): This endpoint uses your custom inverted index to return ranked search results based on the query. It also accepts `query` for the search term and `k` for the number of results to return.

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

### Report

#### Introduction

This project aims to understand and apply search and information retrieval algorithms based on content. 
The project is divided into two parts: 
a) optimal construction of an Inverted Index for text search and retrieval tasks and 
b) construction of a multidimensional structure to support efficient search and
retrieval of images/audio using characteristic vectors. 
Both implementations will be applied to improve search in a recommendation system.

#### Part 1: Construction of the Textual Inverted Index (Full-Text Search)

##### Backend

1. **Implementation of the inverted index using the ranking retrieval model for free-text queries.**
    - **Preparation:**
        - A dataset from Kaggle is used.
    - **Preprocessing:**
        - Tokenization
        - Stopwords filtering
        - Stemming
    - **Index Construction:**
        - Structure the inverted index to store TF-IDF weights.
        - Calculate the document norms once and save them to reuse when applying cosine similarity.
        - Construct the index in secondary memory for large data collections using single-pass in-memory indexing.
        - For the PostgreSQL, an GIN index is created on the search_vector column.
    - **Query:**
        - The query is a natural language phrase.
        - Scoring is obtained by applying cosine similarity on the inverted index in secondary memory.
        - The retrieval function should return the top-k documents closest to the query.

##### Experiment

1. **Measure the performance of your implementation compared to PostgreSQL.**

| N  | MyIndex (Time) | PostgreSQL / MongoDB (Time) |
|----|----------------|-----------------------------|
| 1000  |                |                             |
| 2000  |                |                             |
| 4000  |                |                             |
| 8000  |                |                             |
| 16000 |                |                             |
| 32000 |                |                             |
| 64000 |                |                             |
| ...   |                |                             |
