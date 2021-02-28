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
        self.Casting_Assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU5ZGI0YTdjNjMwMDY4OGM3N2UyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg5NTQyLCJleHAiOjE2MTQ0OTY3NDIsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.NRlDyTQb3Q50lGVo_SlqLHewL6ayKYEpEf63YcVGtZpeHDqhyEOZm0155fR4bn-o9J4WtGz_PeyEAx6FRt_VkZrP7mwa_bFtgqSmWxE4VJO06Ct3-BXTKszeskeO9Dftq4jUFYS8pLOr8ftXy1qpkx8V5GZlCo8dONlEtZYkCnaIM_HdtEu53lHgCwiw_BWP7tS407zShWoynKhVMEmKp0KFQmFAKTtPqTJgsyqVPrcHTKygvJ9Ba6zKyq_wuY0js5p8-fuH5DqKFSdu2C7b9A6dWjq6I49L3YfeeDcri1l4uaUY2eWwI-by-FELV1sjfnOR9Ynr8w8Sm4JgJwHe2g'
        self.Casting_Director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4ZWY5MGU0NDIwMDcwMzhiZDYyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg5NTM2LCJleHAiOjE2MTQ0OTY3MzYsImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.sWfgVd6f7by8VoLFVe_NvS_E2EZfBfgdIPK1Zb2EQvGm0MtlCobEDPWJyTlXFgQ4OqToMrd65M4RHiS3X7hXPvQYdT5s7ek3qkdB9gYwzHvIndyBvnUPNnTtoeW7HUmhPJ1znHq7n2P9mhE2P-XgNnxfbytnWTBkNHi9z4lrrkcnYQ9d00T5emsWJrlBHSUHJfEfhkPbxJ-99Nrz7hwRD1gg1FM3TIv_e6Ufarf9wUqo49jfsV7k8jUA0pKUsfr3ib278sdSQPfbqN8P6BjVUZtFSSLfwuxXiGCe72fPHdPCcA2b1-Fw4ekwPwglJZWrdqEdYdcyweiiAfN-MeMb2w'
        self.Executive_Producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijl0NWI3TzY5OEpuU3pqS3V6c1RpTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyZGU4NGRhNTE0MDIwMDcxZmQwMDQyIiwiYXVkIjoiZGV2IiwiaWF0IjoxNjE0NDg5NTM5LCJleHAiOjE2MTQ0OTY3MzksImF6cCI6IjY1Nm5NVng0VXJWR2xUNVp3dXFrdUJJY2lmaE8yeWZLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.HbBURVYGCx6g6QU7nI7x5kW3sv2g7cK2CcLmLkONWoHJGjSu8RoQuMJEOfRMFyyDjzG4taugpp4Aa_j8OIQ46om-Ceq5Ft-g3WNSsYmBoS-HvchYD9ody5TILQsF6F08jP2JlZyayXVrCI0op4iJPHq80usBotRUiBI2YAwtQh0zzG-q91XJUpFQwMqLLoztlg4_rLTPqrs5gApNxqHcjDglGpGyWhTTYbI-VFINs5F5GCFaarDpUj1gz7k8-4d2cAJCdVm4djhgLsfv87Te1CDSMa92HKuBZnNnDKHmkXLTvRqKgkvIQfGTibOMxs1wUJLdV6zCKxzMHgeIEVldag'
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
