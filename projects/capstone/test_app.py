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
        self.Casting_Assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU5ZGI0YTdjNjMwMDY4OGM3N2UyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg1MDUwLCJleHAiOjE2MTQ0OTIyNTAsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.liLVnnuCLzKWq-nV6itjXaYIn_xWdtD_rnA8z9HPDfEAfhDtKiZzSmvp04rB9Qe3GOUmRG-6mehZpPikvjwrASAG9OkHUCNu8cQPxL3jEzMipG6_1MjOTJFEoUUbk_KqzpyCNae81d7_QbaRQc4tw3kBq7mundpDvAjbOz1H4ZgRmSarTI6IQQAJPutEXzbCS17SHXNU7upXyn41urp0tuALZjSyTjEDR-OxUW79LSKU6qGpMyfNs97r6kRfIX-PDvz6tr-H0tBX3aA_bUWnemU1OQiBL5G2qVdChKvesQn74dvjkfNiaV60JUNUTzHJ4HV_xYq5trHBrZuauC49ew'
        self.Casting_Director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4ZWY5MGU0NDIwMDcwMzhiZDYyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg1MDQyLCJleHAiOjE2MTQ0OTIyNDIsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.gnASWSC3qDA-hCjzP4GTz1qDnK3nKgs08vWlKlmw6i-y21CKI734mlvEXqoOVYT7QzZfQu18QPTXVBmUwATI2h5_tO7ze5nHTDM5n7SGATvryNGfDM2P9kNC9DsjZiwSk3x4gylqbW_Rmi-s-Yj7Yf5-hGVXGs550mnrrr1KDp3Wr-lPXiEq50biF58ZTy_-J89U8oHqX-H6K4-v_y0JaktYwSTm-g-7uaQpZKA9hqCjYR8f9fg88eBOYZVs7lMVpHXuWVqC1YF78Pf6vQst_wX-YcZsmk68kk3rK5SutpmKdPwQlQSH402UVC3g9FknQexSXO2lvZFRbX6z6vxBnA'
        self.Executive_Producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4NGRhNTE0MDIwMDcxZmQwMDQyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg1MDQ2LCJleHAiOjE2MTQ0OTIyNDYsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.rauOjNAEt_Lw3VJyDRvRKJAPDbtyKVdZETwh8EFSnjMqXnQdHVcl_lpdd2CW0BzIer3w_cMPBEbmsoNEWrD_O5nPAbfREQEMrQifnlkMOFcgZ8aDi7musFh4UzTbOozqgZkZ9JboVy2TtebIb7TEN16JUUX9vv6o5Ev4VZj5Snfaqpz5sOFXxuzs5BHW8s8wF4Yu3bLY78nxX6-0-Bn259lxD-FOFqaWLagR389_Kh3zTpqJhGNgsW5lZGVXmq5YCJymq3RYp0_gfQKQ3-Zdh8mwfnkAALu42dBHZLX3MbQorMaFNsEQCBy3gsK03w64y3l0v4xgh7uVcPmF1FKscA'
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

    def test_404_sent_requesting_invalid_endopint_actors(self):
        res = self.client().get('/actors/page=1000', json={'age': 3}, headers={
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

    def test_404_sent_requesting_invalid_endopint_movies(self):
        res = self.client().get('/movies/page=1000', json={'title': "Detictive Conan"}, headers={
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
        self.assertEqual(actor.longActor()['name'],'Zoro')

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
        self.assertEqual(movie.longMovie()['title'], 'Attack on titan')

    def test_400_if_edit_movie_failed(self):
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.Executive_Producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    # delete actor

    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.Casting_Director_token)
    #     })
    #     data = json.loads(res.data)

    #     actor = Actor.query.filter(Actor.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)
    #     self.assertEqual(actor, None)

    # def test_422_if_actor_does_not_exist(self):
    #     res = self.client().delete('/actors/200', headers={
    #         'Authorization': "Bearer {}".format(self.Casting_Director_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # # delete movie
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.Executive_Producer_token)
    #     })
    #     data = json.loads(res.data)

    #     movie = Movie.query.filter(Movie.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1) 
    #     self.assertEqual(movie, None)

    # def test_422_if_movie_does_not_exist(self):
    #     res = self.client().delete('/movies/200', headers={
    #         'Authorization': "Bearer {}".format(self.Executive_Producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
