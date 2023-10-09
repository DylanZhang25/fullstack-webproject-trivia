import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db
from dotenv import load_dotenv
import logging


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"

        load_dotenv()
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')

        DB_PATH = (
            "postgresql+psycopg2://{user}:{password}@{host}/{database}"
            .format(
                user=db_user,
                password=db_password,
                host=db_host,
                database=self.database_name
            )
        )

        """
        The given code "db.init_app(self.app)" here will create a error:
        "RuntimeError: A 'SQLAlchemy' instance has already been registered
        on this Flask app. Import and use that instance instead."
        """
        self.app_context = self.app.app_context()
        self.app_context.push()

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        self.app_context.pop()
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    # Test @app.route('/questions', methods=['GET'])
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # def test_500_when_server_maintenance(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 500)
    #     self.assertFalse(data['success'])
    #     self.assertEqual(data['message'], 'Internal Server Error')

    # Test @app.route('/questions', methods=['GET'])
    def test_get_all_questions_and_paginate_them(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_if_failed_to_get_all_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Test @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def test_delete_a_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_if_failed_to_delete_a_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    # Test @app.route('/questions', methods=['POST'])
    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'abcde',
            'answer': 'abcde',
            'category': 2,
            'difficulty': 2
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_422_if_failed_to_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'abcde',
            'answer': 'abcde',
            'category': 2,
            'difficulty': None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # Test @app.route('/questions/search', methods=['POST'])
    def test_search_a_question(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'actor'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    def test_404_if_failed_to_search_a_question(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'abcdefg'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    # Test
    # @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    def test_404_if_failed_to_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    # test @app.route('/quizzes', methods=['POST'])
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [21],
            'quiz_category': {"type": "Science", "id": "1"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_422_if_failed_to_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [21],
            'quiz_category': None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
