# API Documentation

A RESTful API is used to connect the front-end and back-end via JavaScript. The API is described below.

The API is at `/api/v1.0/`.

## API Endpoints

### User

| Action               | Method | Endpoint     | Response           | Notes |
|----------------------|--------|--------------|--------------------|---|
| Get a user's details | GET    | `/user/<id>` | [User object](#user-object) |
| Create a user | POST | `/user` | HTTP/405 Method Not Allowed | Not implemented |
| Update a user | PUT | `/user` | HTTP/405 Method Not Allowed | Not implemented |


### Session

| Action | Method | Endpoint | Data | Response | Authorization |
|---|---|---|---|---|---|
| Log a user in | POST | `/session` | [Credentials object](#credentials-object) | [Token object](#token-object) | Not required |
| Log a user out | DELETE | `/session` | | | Required |



## API Objects

### Credentials object

| Field | Type | Optionality | Notes |
|---|---|---|---
| `email` | String | Required | User's registered email address |
| `password` | String | Required | User's password |


### Token object

| Field | Type | Optionality | Explanation |
|---|---|---|---|
| `access_token` | String | Required | JSON web token that can be used to authorize the user. |

When sending requests to protected API endpoints, send the `access_token` part of this object in the `Authorization` header.

| Header | Value |
|---|---|
| `Authorization` | `Bearer <authorization_token>` |


### User object

| Field  | Type   | Explanation  |
|-------|--------|--------------|
| `id`    | int    | User ID      |
| `name`  | String | User's name  |
| `email` | string | User's email |