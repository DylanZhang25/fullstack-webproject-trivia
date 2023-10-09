import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import db, setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # add error log messages to terminal
    # handler = StreamHandler()
    # handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(handler)

    with app.app_context():
        setup_db(app)

    """
    @TODO1: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO2: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    """
    @TODO3:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in categories]

            return jsonify({
                'success': True,
                'categories': formatted_categories
            })

        except BaseException:
            abort(500)

    """
    @TODO4:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.

    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            if page > 10:
                abort(404)
            
            start_index = (page - 1) * QUESTIONS_PER_PAGE
            end_index = start_index + QUESTIONS_PER_PAGE

            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]

            categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in categories]

            total_questions = len(questions)
            current_category = None

            return jsonify({
                'success': True,
                'questions': formatted_questions[start_index:end_index],
                'total_questions': total_questions,
                'categories': formatted_categories,
                'current_category': current_category
            })

        except BaseException:
            abort(404)

    """
    @TODO5:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            if question_id < 0:
                raise Exception("Invalid question ID")

            question = Question.query.get(question_id)
            if question is None:
                abort(404)

            # question.delete()
            db.session.delete(question)
            db.session.commit()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except BaseException:
            abort(404)

        finally:
            db.session.close()

    """
    @TODO6:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
    appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_a_new_question():
        try:
            request_data = request.get_json()
            # Get questions, answers, difficulty and classification from
            # request data
            question = request_data.get('question')
            answer = request_data.get('answer')
            category = request_data.get('category')
            difficulty = request_data.get('difficulty')

            if question is None or answer is None or category is None \
                    or difficulty is None:
                abort(422)

            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty)

            # Add the new question to the database
            db.session.add(new_question)
            db.session.commit()

            return jsonify({
                'success': True,
                'created': new_question.id
            })

        except BaseException as e:
            abort(422)

        finally:
            db.session.close()

    """
    @TODO7:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def post_questions_search_request():
        try:
            request_data = request.get_json()
            search_term = request_data.get('searchTerm')

            if search_term is None:
                abort(422)

            questions = db.session.query(Question).filter(
                Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            if len(formatted_questions) > 0:
                return jsonify({
                    'success': True,
                    'total_questions': len(questions),
                    'questions': formatted_questions
                })
            else:
                abort(404)

        except BaseException:
            abort(404)

        finally:
            db.session.close()

    """
    @TODO8:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)

            if category is None:
                abort(404)

            questions = db.session.query(Question).filter(
                Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]

            if len(formatted_questions) > 0:
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(questions),
                    'current_category': category.type
                })
            else:
                abort(404)

        except BaseException:
            abort(404)

        finally:
            db.session.close()

    """
    @TODO9:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        try:
            request_data = request.get_json()
            previous_questions = request_data.get('previous_questions')
            quiz_category = request_data.get(
                'quiz_category')  # {"type":"History","id":"3"}

            if quiz_category is None or previous_questions is None:
                abort(422)
                
            if quiz_category['id'] == 0:
                questions = db.session.query(Question).all()
            else:
                questions = db.session.query(Question).filter(
                    Question.category == quiz_category['id']).all()

            formatted_questions = [question.format() for question in questions]
            # Get the questions that have not been asked before in the
            # specified category
            available_questions = [
                question for question in formatted_questions
                if question['id'] not in previous_questions
            ]

            # If there are no more questions in that category, return None
            if len(available_questions) == 0:
                return jsonify({
                    'success': True,
                    'question': None
                })

            # Get a random question from the specified category
            random_question = random.choice(available_questions)

            return jsonify({
                'success': True,
                'question': random_question
            })

        except BaseException:
            abort(422)

        finally:
            db.session.close()

    """
    @TODO10:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # error handlers for all expected errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500
    
    return app
