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
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',\
       'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', \
       'GET, POST, PUT, DELETE, OPTIONS') 
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def get_categories():
    categories = Category.query.all()
    categories = {category.id:category.type for category in categories}
    return jsonify({
        "success": True,
        "categories": categories,
        "total_categories": len(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  def paginate_response(page, questions):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    current_question = questions[start:end]
    return current_question

  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, int)
    questions = Question.query.all()
    total_questions  = len(questions)
    questions = paginate_response(page, questions)
    if not questions: abort(404)
    categories = Category.query.all()
    categories = {category.id:category.type for category in categories}
    return jsonify({'success': True,
        'questions': questions,
        'page': page,
        'total_questions': total_questions,
        'categories': categories,
        'current_category': "Null"
    })
  '''TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route("/questions/<int:question_id>", methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if not question: abort(404)
    question.delete()
    return jsonify({
      "success": True,
      "deleted_id": question_id
    })
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    payload = request.get_json()
    question = payload.get('question', '')
    answer = payload.get('answer','')
    category =  payload.get('category', '')
    difficulty = payload.get('difficulty', '')
    if not (question and answer and category and difficulty): abort(422)
    new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
    new_question.insert()
    question_id = new_question.id
    return jsonify({
      "success": True,
      "question_id": question_id
    })

  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  

  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    payload = request.get_json()
    search_term = payload.get('searchTerm', '')
    if not search_term: abort(422)
    questions = [question.format() for \
       question in Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()]
    return jsonify({
      "success": True,
      "total_questions": len(questions),
      "questions": questions,
      "current_category": "Null"
    })
  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id, paginate=True):
    page = request.args.get('page', 1, int)
    category = Category.query.filter_by(id=category_id).first()
    if not category: abort(404)
    questions = Question.query.filter_by(category=str(category.id)).all()
    total_questions = len(questions)
    if paginate: 
      questions = paginate_response(page, questions)
    else:
      return [question.format() for question in questions]
    return jsonify({'success': True,
        'questions': questions,
        'page': page,
        'total_questions': total_questions,
        'current_category': category_id
    })
  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    payload = request.get_json()
    previous_questions = payload.get("previous_questions", []) 
    category = payload.get("quiz_category",'').get('id','')
    if category:
      questions = get_questions_by_category(category, paginate=False)
    else: 
      questions = [question.format() for question in Question.query.all()]
    if previous_questions:
      questions = [question for question in questions if question['id'] not in previous_questions]
    random_question =  random.choice(questions) if questions else False
    return jsonify({
      "success": True,
      "question": random_question
    })
  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
      }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
      }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request error"
    }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error"
    }), 500
  return app

    