import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Which is the capital of Saudi Arabia?',
            'answer': 'Riyadh',
            'difficulty': 1,
            'category': '3'
        }
        self.search_data = {
            'searchTerm': 'largest lake in Africa',
        }
        self.quiz_data = {
            'previous_questions': [3, 4],
            'quiz_category': {
                'type': 'Geography',
                'id': 3
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):

        # make request and process response
        response = self.client().get('/categories')
        data = json.loads(response.data)
        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        """Tests question pagination success"""

        # get response and load data
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that total_questions and questions return data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_delete_question(self):
        response = self.client().delete('/questions/12')
        data = json.loads(response.data)
        question = Question.query.filter(Question.id == 12).one_or_none()

        if response.status_code == 422:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(data['deleted'], 12)

    def test_create_new_question(self):
        """Tests question pagination success"""
        # get response and load data
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_400_if_question_creation_not_allowed(self):
        """Tests question pagination success"""

        # get response and load data
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_search_questions(self):
        """Test for searching for a question."""

        # make request and process response
        response = self.client().post('/questions/search', json=self.search_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_questions_fail(self):
        """Test for searching for a question."""

        # make request and process response
        response = self.client().post('/questions/search', json='sdfghjmnbhyguj')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        """Test for getting questions by category."""

        # make a request for the Sports category with id of 6
        response = self.client().get('/categories/3/questions')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Geography')

    def test_invalid_category_id(self):
        """Test for invalid category id"""

        # request with invalid category id 1987
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        # Assertions to ensure 422 error is returned
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_play_quiz_questions(self):
        """Tests playing quiz questions"""

        # make request and process response
        response = self.client().post('/quizzes', json=self.quiz_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # Ensures previous questions are not returned
        self.assertNotEqual(data['question']['id'], 3)
        self.assertNotEqual(data['question']['id'], 4)

    def test_no_data_to_play_quiz(self):
        """Test for the case where no data is sent"""

        # process response from request without sending data
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
