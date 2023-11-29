# Authly Backend

with fastapi

Python Enviroment:
<https://python-poetry.org/>

## Mongo Schema

create db if selfhosted
in the db collections:

- Admin collection
- Users collection
- Applications collection

user/ applications in a collection also get there own object ids (`new ObjectId()`)

### Bubble Collection

currently:

```json
{
  "_id": {
    "$oid": "exmaple oid of bubble collection"
  },
  "name": "string",
  "settings": {
    "allow_new_user_registration": true,
    "test_settings": "HelloWorld",
    "bliblablu": true
  },
  "application_document_id": "example oid 1",
  "key_document_id": "example oid 2",
  "user_document_id": "example oid 3"
}
```

### Admin collection

currently:

directly ref to the document

```json
{
  "_id": ObjectId("admin_id"),
  "username": "admin_username",
  "email": "admin_email",
  "password": "hashed_password",
  "roles": ["admin"],
  "bubbles": [ObjectId("objectidforbubblea"), ObjectId("objectidforbubbleb")]
}
```

### Users collection

```json
{
  "bubbleA": {
    "_id": "ObjectId(objectidforbubblea)",
    "name": "bubbleA",
    "user": [
      {
        "_id": "ObjectId(user_id_1)",
        "username": "user1",
        "email": "user1@example.com",
        "roles": ["user"],
        "resources": []
      }
    ]
  },
  "bubbleB": {
    "_id": "ObjectId(objectidforbubbleb)",
    "name": "bubbleB",
    "user": [
      {
        "_id": "ObjectId(user_id_1)",
        "username": "user1",
        "email": "user1@example.com",
        "roles": ["user"],
        "resources": []
      }
    ]
  }
}
```

### Applications collection

```json
{
  "bubbleA": {
    "_id": "ObjectId(objectidforbubblea)",
    "name": "bubbleA",
    "applications": [
      {
        "_id": "ObjectId(app_id_1)",
        "name": "App 1",
        "version": "1.0",
        "default_access": "users of bubblea"
      },
      {
        "_id": "ObjectId(app_id_2)",
        "name": "App 2",
        "version": "2.0"
      }
    ]
  },
  "bubbleB": {
    "_id": "ObjectId(objectidforbubbleb)",
    "name": "bubbleB",
    "applications": []
  }
}
```
