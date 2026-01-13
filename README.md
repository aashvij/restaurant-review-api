# Restaurant Review API

## Overview

This is a RESTful API built with FastAPI for managing restaurants and user reviews. It allows users to create, retrieve, and delete restaurants and reviews, with features like rating calculations and data validation.

## Key Features

*   **Restaurant Management:**
    *   Create, retrieve, and list restaurants.
    *   Filter and sort restaurants by cuisine, city, and rating.
*   **Review Management:**
    *   Create, retrieve, and delete restaurant reviews.
    *   Automatic calculation of restaurant average ratings based on reviews.
    *   Update existing reviews.
*   **RESTful Endpoints:** Well-defined endpoints using standard HTTP methods (POST, GET, DELETE).
*   **Data Validation:** Utilizes Pydantic for request and response data validation.
*   **FastAPI Framework:** Built using FastAPI for high performance and automatic API documentation (Swagger UI).

## Tech Stack
- **Framework:** FastAPI
- **Validation:** Pydantic
- **Language:** Python 3.x

## Endpoints

*   **/restaurants/**
    *   `POST`: Create a new restaurant.
    *   `GET`: List restaurants (supports filtering and sorting).
    *   `GET/{restaurant_id}`: Get details of a specific restaurant.
*   **/reviews/**
    *   `POST`: Create a new review for a restaurant (or update existing).
    *   `GET/{review_id}`: Get details of a specific review.
    *   `DELETE/{review_id}`: Delete a review.
*   **/reviews/restaurant/{restaurant_id}**:
    *   `GET`: Get all reviews for a specific restaurant.

## Data Models

*   **Restaurant:** `id`, `restaurant_name`, `cuisine`, `address`, `city`, `country`, `phone_number`, `website`, `zip_code`, `rating`, `created_at`.
*   **Review:** `id`, `rating`, `comment`, `restaurant_id`, `user_id`, `created_at`.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd restaurant-review-api
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Access the API documentation at `http://127.0.0.1:8000/docs`.

## Usage Example (Create a Restaurant)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"restaurant_name": "Delicious Bistro", "cuisine": "Italian", "address": "123 Main St", "city": "Anytown", "country": "USA", "zip_code": "12345"}' \
  http://127.0.0.1:8000/restaurants/
```


## Future Enhancements

*   Database integration (PostgreSQL, etc.) for persistent storage.
*   User authentication and authorization.
*   Restaurant update functionality.
*   Image handling for reviews.
*   Pagination for list endpoints.
*   Advanced search capabilities.
