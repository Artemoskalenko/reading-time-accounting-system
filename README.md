<a name="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#api-endpoints">API Endpoints</a>
    </li>
  </ol>
</details>


#
# About The Project

A system that tracks the time a user spends reading a book, where the user has the ability to start and end a reading session.

## Features

1. For the user
   - Getting information about all available books
   - Getting information about a specific book
   - Start and end a book reading session
   - Getting reading statistics for a specific book
   - Getting general user statistics

2. For admin
   - Create, delete, change books through the admin panel
   - All functions available to the user

3. Celery
   - Daily collection of reading statistics for all users and updating user statistics for the last 7 and 30 days

## Built With
![](https://img.shields.io/badge/python-3.11.4-blue)
![](https://img.shields.io/badge/django-4.2.7-blue)
![](https://img.shields.io/badge/DRF-3.14.0-blue)
![](https://img.shields.io/badge/Celery-5.3.6-blue)
![](https://img.shields.io/badge/flake8-6.1.0-blue)

#
# Getting Started

This is a simple guide how to build up an application locally. Just follow this steps.

## Prerequisites

* Docker (Make sure the docker daemon is running)


## Installation

1. Clone the repo.
   ```sh
   $ git clone https://github.com/Artemoskalenko/reading-time-accounting-system.git
   ```
2. Running a Docker container.
   ```sh
   $ cd reading-accounting-system
   ```
   ```sh
   $ docker-compose build
   ```
   ```sh
   $ docker-compose up
   ```
3. After starting the Docker container, the admin user will be automatically created.
   - Login: `admin`
   - Password: `admin`
   
    **That's all.** Browse [localhost](http://localhost:8000) and you're supposed to see the swagger page:

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Database Structure

![db diagram](/.github/images/diagram.JPG)

## API Endpoints
See auto-generated documentation for API to get all info about available resources and methods.
*Make sure that django server is running.*
- <a href="http://localhost:8000/swagger/">Swagger</a>

### User

#### Session authentication

- Login:
  - **HTTP Method:** GET/POST
  - **URL:** `/api/v1/drf-auth/login/`
  - **Description:** Displays the login page where the user can log into the account.

- Logout:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/drf-auth/logout/`
  - **Description:** Allows the user to log out of the account and go to the login page.

#### Token authentication

- Create User:
  - **HTTP Method:** POST
  - **URL:** `auth/users/`
  - **Description:** Creating a user using API.
  - **Example JSON:**`{"username": "admin", "password": "yourpassword", "email": "youremail@gmail.com"}`

- Login:
  - **HTTP Method:** POST
  - **URL:** `/auth/token/login/`
  - **Description:** Token authorization via API.
  - **Example JSON:**`{"username": "admin", "password": "your_password"}`

- Logout:
  - **HTTP Method:** GET
  - **URL:** `/auth/token/logout/`
  - **Description:** Allows the user to log out of the account.
  - **Required request header:**`{"Authorization": "Token {your_token}"}`

### Book reading API

- List of books:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/books/`
  - **Description:** Displaying a list of all books.
    
- Book details:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/book-details/{book_id}/`
  - **Description:** Displaying information of a specific book by id.

- Start reading session:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/start-reading-session/{book_id}/`
  - **Description:** Starts a reading session for a book with the specified id.

- End reading session:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/end-reading-session/`
  - **Description:** Ends book reading session.

- Book statistics:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/book-reading-statistics/{book_id}/`
  - **Description:** Displaying user statistics for a specific book.

- User statistics:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/user-statistics/`
  - **Description:** Displaying general user statistics.

<p align="right">(<a href="#readme-top">back to top</a>)</p>