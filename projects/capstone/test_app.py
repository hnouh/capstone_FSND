import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the CastingAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.Casting_Assistant_token = os.environ['Casting_Assistant_token']
        self.Casting_Director_token = os.environ['Casting_Director_token']
        self.Executive_Producer_token = os.environ['Executive_Producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_host = os.getenv('DB_HOST', 'localhost:5432')
        self.database_user = os.getenv('DB_USER', 'postgres')
        self.database_password = os.getenv('DB_PASSWORD', 'Ar648898')
        self.database_name = os.getenv('DB_NAME', 'CastingAgency_test')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            self.database_user, self.database_password, self.database_host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_actor = {
                "name": "Luffy",
                "age": "26",
                "gender": "male"
            }

            self.new_movie = {
                "title": "One Piece",
                "releaseDate": "12/02/2010"
            }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """ 
    test each for successful operation and for expected errors.
    """
    # get actors

    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['actors'])) 

    def test_404_sent_requesting_invalid_endopint(self):
        res = self.client().get('/actors?page=1000', json={'age': 3}, headers={
            'Authorization': "Bearer".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # delete actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/200', headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # create actors
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/200', json=self.new_actor, headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    # edit actors
    def test_edit_actor_name(self):
        res = self.client().patch('/actors/2', json={'name':'Zoro'}, headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id==2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'],2) 

    def test_400_if_edit_actor_failed(self):
        res = self.client().patch('/actors/2', headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    ################################################################################

    # get movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['movies'])) 

    def test_404_sent_requesting_invalid_endopint(self):
        res = self.client().get('/movies?page=1000', json={'title': "Detictive Conan"}, headers={
            'Authorization': "Bearer".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # delete movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/200', headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # create movies
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={
            'Authorization': "Bearer".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/200', json=self.new_movie, headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    # edit movies
    def test_edit_movie_title(self):
        res = self.client().patch('/movies/2', json={'title':'Attack on titan'}, headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id==2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'],2) 

    def test_400_if_edit_movie_failed(self):
        res = self.client().patch('/movies/2', headers={
            'Authorization': "Bearer".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

