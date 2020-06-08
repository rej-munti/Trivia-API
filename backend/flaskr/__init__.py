import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={"/": {"origins": "*"}})
  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():

      categories = Category.query.all()
      formatted_category = [category.type for category in categories]
     
      return jsonify({
            'categories':formatted_category
        })

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
      categories = Category.query.all()
      formatted_category = [category.type for category in categories]
      page = request.args.get('page', 1, type=int)
      start = (page - 1)*10
      end = start + 10
      questions = Question.query.all()
      formatted_question = [question.format() for question in questions]
      return jsonify({
            'questions':formatted_question[start:end],
            'total_questions': len(formatted_question),
            'categories': formatted_category
                    })
  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

      question =  Question.query.get(question_id)
      question.delete()

      return jsonify({
            'deleted': question_id
        })
  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_questions():

      question = request.json.get('question')
      answer = request.json.get('answer')
      category = request.json.get('category')
      difficulty = request.json.get('difficulty')  
      added_question = Question(question, answer, category, difficulty)
      added_question.insert()

      return jsonify({
            'question': added_question.format()
        })

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      body = request.get_json()
      search_term = body.get('searchTerm')
      page = request.args.get('page', 1, type=int)
      start = (page - 1)*10
      end = start + 10
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      formatted_question = [question.format() for question in questions]
      return jsonify({
                'questions':formatted_question[start:end],
                'total_questions': len(questions)
             })
      
  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_based_on_category():
     category = Category.query.get(category_id)
     questions = Question.query.filter(Question.category == category_id).all()
     return jsonify({
             'success':True,
             'response':questions,
             'total_questions': len(questions)
       })
  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
     body = request.get_json()
     previous_questions = body.get('previous_questions')
     quiz_category = body.get('quiz_category')

     if (quiz_category['id'] == 0):
        questions = Question.query.all()
     else:
        questions = Question.query.filter_by(category=quiz_category['id']).all()
   
     total = len(questions)

     def get_random():
        return questions[random.randrange(0, len(questions), 1)]
     
     question = get_random()

     for x in previous_questions:
       if (x == question.id):
           question = get_random()
       else:
           question = question

     return jsonify({
        'success': True,
        'question': question.format()
        })
      
  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
  return app

    