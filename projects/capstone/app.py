import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from models import setup_db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS app
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # ROUTES
    '''
    implement endpoint
        GET /actors 
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.longActor() for actor in actors]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors
        }), 200

    ''' 
        GET /movies 
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.longMovie() for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        }), 200

    '''
        POST /actors
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_new_actor(jwt):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actors': actor.longActor()
            }), 200

        except Exception:
            abort(422)

    ''' 
        POST /movies 
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_new_movie(jwt):
        body = request.get_json()

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)

        try:
            movie = Movie(title=new_title, releaseDate=new_releaseDate)
            movie.insert()

            return jsonify({
                'success': True,
                'movies': movie.longMovie()
            }), 200

        except Exception:
            abort(422)

    ''' 
        PATCH /actors/<id>
            where <id> is the existing model id 
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):

        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.longActor()]
            }), 200

        except Exception:
            abort(400)

    ''' 
        PATCH /movies/<id> 
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):

        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = body.get('title')
            if 'releaseDate' in body:
                movie.releaseDate = body.get('releaseDate')

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.longMovie()]
            }), 200

        except Exception:
            abort(400)

    '''
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:/actors' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200

        except Exception:
            abort(422)

    '''
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:/movies' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200

        except Exception:
            abort(422)

    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
app = create_app()

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
'''
