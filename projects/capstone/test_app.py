import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app

# from flaskr import create_app
from models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the CastingAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.Casting_Assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU5ZGI0YTdjNjMwMDY4OGM3N2UyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDc3NDkxLCJleHAiOjE2MTQ0ODQ2OTEsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.KUeo7UTohbyg8zDRokbwXgYiN8ZNleRzoU5IHsBgjX75W68SvGY3YggYoH-3RkEoAwDV87FzOcyyAa8-b4VsjS3Z5a_OkA_nzWpiIZW0R-hWYU77g1OCtHU_TVHU4-ngyODcxkr--eJVjxa683wfSjLRH4lAfT5zgZ55uY8t_GVoPhPDhBOCWn8wEhFtaFir1F6_CwIlTzNP138UrKIfuvhFt5Ly2z3IDc87PhZIEg6xG6BmeiBvnpjDywtpY8QeMKcpvWw6fXFXR6UjVvYFOEU7SEoLMnIga6hqLbAFGzCLd7yD74wxgwy1xAELOjxUDzOJE3xMDMLWertYIpIfhg'
        self.Casting_Director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4ZWY5MGU0NDIwMDcwMzhiZDYyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDc3NDk1LCJleHAiOjE2MTQ0ODQ2OTUsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.g3YfM-DN_fZhjFTOHZ6mguRvnZgJ8s5uDOwKTDdqIJel0WhiwQk7lf5QLqIL2Ey39bp4GYBosKcdD3DJEKqlP3LixOkpfdHlGWdYI9dKhGj7NiCmCDQ89jTLehwKs8kZXPzL5CwscyeqELMOzM-I2EVCIpVRyxymkyAnwHzsCLleUHkb18KBMszfT-3YWQblAA4hDKTaOHfPIiy9N-09x-a_coMsF96jiSrSNxHJCwUodheFyabwu4r7_Z0w09lcXXg5Gk8S9hU9A7PsR9emHgFWQXpMC-_5UZ8m8WS0b4B7Rwr4VmKzbpWlxOQDfKHXEWWU6iGBo-mbvfN4K7NReQ'
        self.Executive_Producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4NGRhNTE0MDIwMDcxZmQwMDQyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDc3NDg1LCJleHAiOjE2MTQ0ODQ2ODUsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.oEmrqPaEtA_HSX6iYwz8mi-1w660a5XS143Ygq66wtiyi42eRKEdXAkfM8KK22ONem0YNVYxj-kfjlKmQ_wpb5DCa4N0h0ZPAHfgWnIb1K8chUyUowujO7X3QYwQ10SGuxGagRSo5czn7qD3IechOo_EvMTRmWV2brLM0Fwj4h8gxxU28SDG1ssQocSFEwfO1bBz4yv3nDDB0q5q4dnlCz9R8C8aS5JO5mAsvOsF-Tfk6AJXp-qoKjqXgMQFSRMwx30NoYUmufALnxppCRWdXZWGu6fL_y5tjGfDBttYCHxuoYEToZ5s3Y_7Oz3h_Zq8wc3U6FFfCl2bGoaGjXlK1w'
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_host = os.getenv('DB_HOST', 'localhost:5432')
        # self.database_user = os.getenv('DB_USER', 'postgres')
        # self.database_password = os.getenv('DB_PASSWORD', 'Ar648898')
        # self.database_name = os.getenv('DB_NAME', 'CastingAgency_test')
        # self.database_path = 'postgresql://{}:{}@{}/{}'.format(
        # self.database_user, self.database_password, self.database_host, self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format('naogqmhsxmzeuo', 'b7caf81f5e3c5629346356fc2f0e96c0ceb835acb306a45db94c86c26c0b5bff',
                                                             'ec2-54-220-35-19.eu-west-1.compute.amazonaws.com:5432', 'ddstbpre9t8qo0')
        # self.database_path = 'postgresql://{}:{}@{}/{}'.format(
        #     self.database_user, self.database_password, self.database_host, self.database_name)
        
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
    # create actors

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={
            'Authorization': "Bearer {}".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/200', json=self.new_actor, headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # create movies
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/200', json=self.new_movie, headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # get actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_invalid_endopint(self):
        res = self.client().get('/actors?page=1000', json={'age': 3}, headers={
            'Authorization': "Bearer {}".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # get movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_invalid_endopint(self):
        res = self.client().get('/movies?page=1000', json={'title': "Detictive Conan"}, headers={
            'Authorization': "Bearer {}".format(self.Casting_Assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # edit actors
    def test_edit_actor_name(self):
        res = self.client().patch('/actors/1', json={'name': 'Zoro'}, headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })

        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.longActor()['name'],1 )

    def test_400_if_edit_actor_failed(self):
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # edit movies
    def test_edit_movie_title(self):
        res = self.client().patch('/movies/1', json={'title': 'Attack on titan'}, headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })

        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.longMovie()['title'], 1)

    def test_400_if_edit_movie_failed(self):
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    # delete actor

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.Casting_Director_token)
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
            'Authorization': "Bearer {}".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # delete movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
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
            'Authorization': "Bearer {}".format(self.Casting_Director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
