## Users Table

| Column           | Data Type | Constraints              |
|------------------|-----------|--------------------------|
| id               | Integer   | Primary Key              |
| email            | Text      | Not Null, Unique         |
| username         | Text      | Not Null, Unique         |
| image_url        | Text      | Default                  |
| header_image_url | Text      | Default                  |
| bio              | Text      |                          |
| location         | Text      |                          |
| password         | Text      | Not Null                 |

## Follows Table

| Column                    | Data Type | Constraints                         |
|---------------------------|-----------|-------------------------------------|
| user_being_followed_id    | Integer   | Foreign Key (users.id), Primary Key |
| user_following_id         | Integer   | Foreign Key (users.id), Primary Key |

## Messages Table

| Column    | Data Type   | Constraints                          |
|-----------|-------------|--------------------------------------|
| id        | Integer     | Primary Key                          |
| text      | String(140) | Not Null                             |
| timestamp | DateTime    | Not Null, Default                    |
| user_id   | Integer     | Foreign Key (users.id), Not Null     |

## Likes Table

| Column     | Data Type | Constraints                                   |
|------------|-----------|-----------------------------------------------|
| id         | Integer   | Primary Key                                   |
| user_id    | Integer   | Foreign Key (users.id), On Delete Cascade     |
| message_id | Integer   | Foreign Key (messages.id), Unique, On Delete Cascade |


Relationships
User - Follows: Many-to-Many (A user can follow many users, and a user can be followed by many users)
User - Messages: One-to-Many (A user can have many messages)
User - Likes: Many-to-Many (A user can like many messages, and a message can be liked by many users)

## Visual Representation 

Users
-------------------
id (PK)
email
username
image_url
header_image_url
bio
location
password

Follows
-------------------
user_being_followed_id (FK, PK)
user_following_id (FK, PK)

Messages
-------------------
id (PK)
text
timestamp
user_id (FK)

Likes
-------------------
id (PK)
user_id (FK)
message_id (FK, unique)


Why follows Table has Two Foreign Keys to the Same Table
The follows table has two foreign keys to the users table because it represents a many-to-many relationship where a user can follow another user. user_being_followed_id is the user who is being followed, and user_following_id is the user who is following. This setup allows the same user to be both a follower and a followee.


### Step Seven: Research and Understand Login Strategy

# How is the logged in user being kept track of?
-The logged-in user is kept track of using the session. When a user logs in, their user ID is stored in the session under the key CURR_USER_KEY. This allows the application to remember which user is logged in between requests.

# What is Flask’s g object?
-Flask’s g object is a global namespace for holding any data during an application context. It is a way to store data that can be shared across different parts of the application during a request lifecycle. It is not persistent and is reset with each request.

# What is the purpose of add_user_to_g?
-The purpose of add_user_to_g is to check if a user is logged in by looking for the user ID in the session. If the user ID is found, it fetches the user from the database and assigns it to g.user. This makes the logged-in user easily accessible throughout the request.

# What does @app.before_request mean?
-@app.before_request is a decorator that registers the decorated function to be run before each request. This means that the function add_user_to_g will be executed before every request to ensure that the current user is set in the global g object if they are logged in.