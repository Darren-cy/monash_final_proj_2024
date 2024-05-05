# API Documentation

A RESTful API is used to connect the front-end and back-end via JavaScript. The API is described below.

The API is at `/api/v1.0/`.

## API Endpoints

### User

| Action               | Method | Endpoint     | Response                    | Notes           |
|----------------------|--------|--------------|-----------------------------|-----------------|
| Get a user's details | GET    | `/user/<id>` | [User object]               |                 |


### Session

| Action         | Method | Endpoint   | Data                 | Response                      | Authorization |
|----------------|--------|------------|----------------------|-------------------------------|---------------|
| Log a user in  | POST   | `/session` | [Credentials object] | [Token object](#token-object) | Not required  |
| Log a user out | DELETE | `/session` |                      |                               | Required      |

### Documents

| Action                  | Method | Endpoint                  | Data | Response          | Authorization |
|-------------------------|--------|---------------------------|------|-------------------|---------------|
| Get a list of documents | GET    | `/document`               |      | Document list     | Not required  |
| Get a specific document | GET    | `/document/<id>`          |      | [Document object] | Not required  |
| Download a document     | GET    | `/document/<id>/download` |      | File stream       | Not required  |
| Upload a document       | POST   | `/document`               | *    | [Document object] | Required      |

* Multipart form with one file with name `file`.

### Authors

| Action                | Method | Endpoint       | Data            | Response        |
|-----------------------|--------|----------------|-----------------|-----------------|
| Get a list of authors | GET    | `/person`      |                 | [Person object] |
| Get a specific author | GET    | `/person/<id>` |                 | [Person object] |
| Create an author      | POST   | `/person`      | [Person object] | [Person object] |


### Assessments
| Action                    | Method | Endpoint           | Data | Response | Authorization |
|---------------------------|--------|--------------------|------|----------|---------------|
| Get a list of assessments | GET    | `/assessment`      |      |          | Not required  |
| Get a specific assessment | GET    | `/assessment/<id>` |      |          | Not required  |
| Create an assessment      | POST   | `/assessment`      |      |          | Required      |


### Submissions

| Action                                      | Method | Endpoint                      | Data | Response |
|---------------------------------------------|--------|-------------------------------|------|----------|
| Get a list of all submissions               | GET    | `/submission`                 |      |          |
| Get a specific submission                   | GET    | `/submission/<id>`            |      |          |
| Get a list of submissions for an assessment | GET    | `/assessment/<id>/submission` |      |          |
| Create a submission                         | POST   | `/assessment/<id>/submission` |      |          |


## API Objects

### Credentials object

[Credentials object]: #credentials-object

| Field      | Type   | Optionality | Notes                           |
|------------|--------|-------------|---------------------------------|
| `email`    | String | Required    | User's registered email address |
| `password` | String | Required    | User's password                 |

### Token object

| Field          | Type   | Optionality | Explanation                                            |
|----------------|--------|-------------|--------------------------------------------------------|
| `access_token` | String | Required    | JSON web token that can be used to authorize the user. |

When sending requests to protected API endpoints, send the `access_token` part of this object in the `Authorization` header.

| Header          | Value                          |
|-----------------|--------------------------------|
| `Authorization` | `Bearer <authorization_token>` |


### User object

[User object]: #user-object

| Field   | Type   | Explanation  |
|---------|--------|--------------|
| `id`    | Int    | User ID      |
| `name`  | String | User's name  |
| `email` | string | User's email |

### Document object

[Document object]: #document-object

| Field         | Type   | Explanation                                               |
|---------------|--------|-----------------------------------------------------------|
| `id`          | Int    | Document's ID                                             |
| `name`        | String | Document's filename                                       |
| `type`        | String | Document's mime type                                      |
| `ctime`       | String | Creation time of the document                             |
| `size`        | Int    | Filesize in bytes                                         |
| `owner.id`    | Int    | File owner's ID                                           |
| `owner.name`  | String | File owner's name                                         |
| `downloadURL` | String | URL from which the contents of the file may be downloaded |


### Person object

[Person object]: #person-object

| Field | Type   | Explanation                |
|-------|--------|----------------------------|
| id    | Int    | Person object's ID         |
| name  | String | Person's name              |
| uri   | String | URI to retrieve the Person |