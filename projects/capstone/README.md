# Full Stack Capstone Project

## About the Application   

Casting Agency app :

1) Add actors & movies. 
2) Display actors & movies. 
3) Edit actors & movies. 
4) Delete actors & movies..

**Install the dependencies:**
```
pip install -r requirements.txt
```

### Tests

```
py test_app.py
```

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return three error types when requests fail:
- 400: bad request
- 404: resource Not Found
- 405: method not allowed
- 422: unprocessable

### Endpoints 



#### GET /actors
- General:
    - Returns a list of actors, success value.
- Sample: `curl https://casting-agency-5.herokuapp.com/actors`
``` 
  "actors": [
    {
      "age": 20,
      "gender": "Male"
      "name": "Eren",
      "id": 1,
    },
    {
      "age": 20,
      "gender": "Female
      "name": "Mikasa,
      "id": 2,
    }
  ],
  "success": true
}
```
#### GET /movies
- General:
    - Returns a list of movies, success value.
- Sample: `curl https://casting-agency-5.herokuapp.com/actors`
``` 
  "movies": [
    {
            "id": 1,
            "releaseDate": "Sun, 07 Apr 2013 00:00:00 GMT",
            "title": "Attack on titan"
        },
    {
            "id": 2,
            "releaseDate": "Wed, 08 Jan 1996 00:00:00 GMT",
            "title": "Detective conan"
        }
  ],
  "success": true
}
```
#### POST /actors
- General:
    - Creates a new actor using name, age, gender. Returns the created actor, success value.
- `curl https://casting-agency-5.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d '{"name":"Conan", "age":"18", "gender":"Male"}'`
```
{
  "created": 52, 
  "actors": {
        "age": 18,
        "gender": "Male",
        "id": 4,
        "name": "Conan"
    },
    "success": true
}
```
#### POST /movies
- General:
    - Creates a new actor using title, releaseDate. Returns the created movie, success value.
- `curl https://casting-agency-5.herokuapp.com/movies -X POST -H "Content-Type: application/json" -d '{"title":"Ano hana", "releaseDate":"12/02/2009"}'`
```
{
  "movies": {
        "id": 3,
        "releaseDate": "Wed, 02 Dec 2009 00:00:00 GMT",
        "title": "Ano hana"
    },
    "success": true
}
```
#### Edit /actors/{actor_id}
- General:
    - Edit actors, sent the request in the body. Returns edited actor. 
- `curl https://casting-agency-5.herokuapp.com/actors/4 -X PATCH -H "Content-Type: application/json" -d '{"name":"Eren"}'`
```
{
  "actors": [
        {
            "age": 20,
            "gender": "Male",
            "id": 4,
            "name": "Eren"
        }
    ],
    "success": true
}
```
#### Edit /movies/{movie_id}
- General:
    - Edit movies, sent the request in the body. Returns edited movie. 
- `curl https://casting-agency-5.herokuapp.com/movies/4 -X PATCH -H "Content-Type: application/json" -d '{"title":"AOT"}'`
```
{
    "movies": [
        {
            "id": 2,
            "releaseDate": "Wed, 02 Dec 2009 00:00:00 GMT",
            "title": "AOT"
        }
    ],
    "success": true
}
```
#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns the id of the deleted actor, success value. 
- `curl -X DELETE https://casting-agency-5.herokuapp.com/actors/3`
```
{
    "deleted": 3,
    "success": true
}
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted movie, success value. 
- `curl -X DELETE https://casting-agency-5.herokuapp.com/movies/2`
```
{
    "deleted": 2,
    "success": true
}
```
## Acknowledgements 
The awesome team at Udacity and all of the classmate, soon to be full stack extraordinaires! 