# PriziRadar API

PriziRadar API allows users to retrieve random comments from Instagram posts.

## Table of Contents

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Documentation](#documentation)
- [Contact Information](#contact-information)

## About the Project

This API serves the purpose of fetching random comments from Instagram posts. To use this API, you need to have a developer account on Meta for Developers, create an app following the [tutorial](https://developers.facebook.com/docs/development/create-an-app/?locale=en_US). Additionally, you should have a Facebook account, a Facebook page, and an Instagram professional account connected to this page.

## Getting Started

### Prerequisites

- Facebook Account
- Meta for Developers Developer Account
- Facebook Page
- Instagram Professional Account connected to the Facebook Page

### Installation

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:lin4lins/PriziRadarAPI.git
    cd PriziRadarAPI
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run with Docker:**

    - Ensure Docker Engine is running (use Docker Desktop app).
    
    - In the terminal, run the following command:

        ```bash
        docker-compose up
        ```

Now your PriziRadar API should be up and running using Docker.

## Usage

To interact with the PriziRadar API, you can make HTTP POST requests with a JSON body. The API responds with JSON-formatted data. Follow the guidelines below to make a request:

### Making a POST Request

- **Endpoint:** `http://localhost:8000` or your endpoint
- **Request Methods:** POST, GET, DELETE
- **Request Body:** JSON

## Endpoints

### 1. POST /login/

Authenticate and obtain a connection token.

#### Parameters

- **Data (Body)**
    ```json
    {
      "ig_token": "your_instagram_token"
    }

**Responses:**

- **Success Response:**
  - *Status Code:* 200 OK
  - *Example Response:*
    ```json
    {
      "token": "your_access_token",
      "user": {
        "username": "example_user",
        "profile_picture_url": "https://example.com/profile_picture.jpg"
      }
    }
    ```

  - *Description:* Successful authentication response. The `token` is the access token for the PriziRadar API, and `user` contains user details, including username and profile picture URL.

- **Error Response:**
  - *Status Code:* 401 Unauthorized
  - *Example Response:*
    ```json
    {
      "detail": "Incorrect authentication credentials."
    }
    ```
  - *Description:* Error response when the provided Instagram token is invalid.

**Example Usage:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"ig_token": "your_instagram_token_here"}' http://localhost:8000/login/

```

### 2. DELETE /logout/

Log out and invalidate the connection token.

- **Headers:**
  - `Authorization`: Bearer your_access_token

**Responses:**

- **Success Response:**
  - *Status Code:* 204 No Content

- **Error Response:**
  - *Status Code:* 401 Unauthorized
  - *Example Response:*
    ```json
    {
      "detail": "Incorrect authentication credentials."
    }
    ```
  - *Description:* Error response when the provided token is invalid or has expired.

**Example Usage:**

```bash
curl -X DELETE -H "Authorization: Bearer your_token_here" http://localhost:8000/logout/
```

### 3. POST /post/

Get information about an Instagram post by providing its URL.

**Parameters:**

- **Headers:**
    - `Authorization`: Bearer Token

- **URL Parameter:**
    - `url`: The URL of the Instagram post.


**Responses:**

- **Success Response:**
  - *Status Code:* 200 OK
  - *Example Response:*
    ```json
    {
      "id": "123456789",
      "caption": "This is a post caption.",
      "media_url": "https://photo_url/",
      "comments_count": 35
    }
    ```
  - *Description:* Successful response containing information about the Instagram post, including its ID, caption, media URL, and comments count.

- **Error Response:**
  - *Status Code:* 401 Unauthorized
  - *Example Response:*
    ```json
    {
      "detail": "Incorrect authentication credentials."
    }
    ```
  - *Description:* Error response when the provided token is invalid or has expired.

**Example Usage:**

```bash
curl -X POST -H "Authorization: Bearer your_token_here" http://localhost:8000/post?url=https://instagram.com/p/C/123test/
```

### 4. Get Random Comment from Post

#### GET /post/{post_id}/random-comment

Get a random comment from a specific Instagram post.

**Parameters:**

- **Path Parameter:**
  - `post_id`: The ID of the Instagram post.

- **Query Parameter:**
  - `count` (optional): The number of random comments to retrieve (default is 1).

**Responses:**

- **Success Response:**
  - *Status Code:* 200 OK
  - *Example Response:*
    ```json
    [
      {
        "place": 1,
        "username": "comment_author",
        "avatar_url": "url",
        "text": "Test comment"
      }
    ]
    ```
  - *Description:* Successful response containing an array of random comments, each with details like place, username, avatar URL, and text.

- **Error Response:**
  - *Status Code:* 404 Not Found
  - *Example Response:*
    ```json
    {
      "detail": "Post not found"
    }
    ```
  - *Description:* Error response when the specified post ID is not found.

**Example Usage:**

```bash
curl http://localhost:8000/post/123456/random-comment?count=3
```

## Documentation

### Detailed API Documentation

For more detailed documentation, including interactive testing and exploration of API endpoints, you can use Swagger/OpenAPI.

- **Swagger Documentation:**
  - [Swagger Documentation](http://0.0.0.0:8000/swagger/)

Swagger provides an interactive API documentation that allows you to explore and test the various endpoints of the PriziRadar API.

Feel free to use Swagger to better understand the API structure and make test requests before integrating it into your application.

## Contact Information

If you have any questions, issues, or feedback regarding the PriziRadar API, feel free to reach out to the project maintainers:

- **Maintainer:** Elina Shramko
- **Email:** elina.vl.shramko@gmail.com

I appreciate your feedback and are here to assist you with any inquiries related to the API.
