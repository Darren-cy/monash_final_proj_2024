# API Documentation

A RESTful API is used to connect the front-end and back-end via JavaScript. The API is described below.

The API is at `/api/v1.0/`.

## Users

| Action               | Method | Endpoint     | Response           |
|----------------------|--------|--------------|--------------------|
| Get a user's details | GET    | /user/\<id\> | A JSON user object |

User objects have the following fields:

| Name  | Type   | Explanation  |
|-------|--------|--------------|
| id    | int    | User ID      |
| name  | String | User's name  |
| email | string | User's email |