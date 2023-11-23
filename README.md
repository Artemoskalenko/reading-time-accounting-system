# Installation

- Cloning the repository

    `git clone https://github.com/Artemoskalenko/reading-time-accounting-system.git`


- Running a docker container:
    ```
    cd reading-accounting-system
    docker-compose build
    docker-compose up
    ```

- Browse `127.0.0.1:8000` or `localhost:8000`

After raising the Docker container, the database will be created automatically, migrations will be applied and the admin user will be created.
- Login: admin
- Password: admin



# Endpoints

## User

### Session authentication

- Login:
  - **HTTP Method:** GET/POST
  - **URL:** `/api/v1/drf-auth/login/`
  - **Description:** Displays the login page where the user can log into the account.

- Logout:
  - **HTTP Method:** GET
  - **URL:** `/api/v1/drf-auth/logout/`
  - **Description:** Allows the user to log out of the account and go to the login page.

### Token authentication

- Create User:
  - **HTTP Method:** POST
  - **URL:** `/api/v1/auth/users/`
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

## Book reading API

- List of books:
  - **HTTP Method:** GET
  - **URL:** `/books/`
  - **Description:** Displaying a list of all books.
    
- Book data:
  - **HTTP Method:** GET
  - **URL:** `/book-details/{book_id}/`
  - **Description:** Displaying information of a specific book by id.

- Start reading session:
  - **HTTP Method:** GET
  - **URL:** `/start-reading-session/{book_id}/`
  - **Description:** Starts a reading session for a book with the specified id.

- End reading session:
  - **HTTP Method:** GET
  - **URL:** `/end-reading-session/`
  - **Description:** Ends book reading session.

- Book statistics:
  - **HTTP Method:** GET
  - **URL:** `/book-reading-statistics/{book_id}/`
  - **Description:** Displaying user statistics for a specific book.

- User statistics:
  - **HTTP Method:** GET
  - **URL:** `/user-statistics/`
  - **Description:** Displaying general user statistics.