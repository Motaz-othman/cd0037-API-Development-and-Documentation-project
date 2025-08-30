from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)



    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS Headers



    with app.app_context():
        db.create_all()

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """




    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        if not categories:
            abort(404)

        categories_map = {c.id: c.type for c in categories}

        return jsonify({
            "success": True,
            "categories": categories_map
        }), 200
    

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():

        selection = Question.query.order_by(-Question.id).all()
        current_questions = pagination(request, selection)
        if not current_questions:
            abort(404)
        categories = Category.query.order_by(Category.id).all()
        categories_map = {c.id: c.type for c in categories}

        return jsonify({
            "success": True,
            "questions": current_questions,          # list of formatted questions
            "total_questions": len(selection),       # total across all pages
            "categories": categories_map,
            "current_category": None
        }), 200
        

    
    def pagination(request,selection):
        page = request.args.get('page',1,type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted = [item.format() for item in selection]
        categories_list = formatted[start:end]

        return categories_list









    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):

        question = Question.query.get(question_id)
        if not question:
            abort(404)

        question.delete()


        return jsonify({
            "success": True,
            "deleted_question": question_id, 

        }), 200
        

    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.


    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """



    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():
        data = request.get_json(silent=True) or {}

        # --- SEARCH PATH ---
        # Frontend sends "searchTerm" (fallback to "search" just in case)
        search = data.get('searchTerm') or data.get('search')
        if search is not None and str(search).strip() != '':
            selection = Question.query.filter(
                Question.question.ilike(f"%{search}%")
            ).order_by(Question.id)

            current_questions = pagination(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": selection.count(),
                "current_category": None
            }), 200

        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')      # stored as string in your model
        difficulty = data.get('difficulty')

        if not question or not answer or category is None or difficulty is None:
            abort(400)
        try:
            difficulty = int(difficulty)
        except (TypeError, ValueError):
            abort(400)

        category = str(category)

        try:
            new_q = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_q.insert()
        except Exception:
            db.session.rollback()
            abort(422)

        return jsonify({
            "success": True,
            "created": new_q.id,
            "question": new_q.format(),
            "total_questions": Question.query.count()
        }), 201
    


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)


        selection = (Question.query
                    .filter(Question.category == str(category_id))
                    .order_by(Question.id))

        current_questions = pagination(request, selection)
        if not current_questions:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,           
            "total_questions": selection.count(),
            "current_category": category_id
        }), 200


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json(silent=True) or {}

        previous = data.get('previous_questions', []) or []
        quiz_category = data.get('quiz_category') or {}
        raw_id = quiz_category.get('id', 0)

        try:
            category_id = int(raw_id)
        except (TypeError, ValueError):
            abort(400)

        query = Question.query

        if category_id != 0:  
            query = query.filter(Question.category == str(category_id))

        if previous:
            query = query.filter(~Question.id.in_(previous))

        question = query.order_by(func.random()).first()

        if question is None:
            return jsonify({
                "success": True,
                "question": None,
                "current_category": category_id
            }), 200

        return jsonify({
            "success": True,
            "question": question.format(),
            "current_category": category_id
        }), 200


    @app.route('/questions/<int:question_id>', methods=['PUT'])
    def update_question(question_id):
        q = Question.query.get(question_id)
        if q is None:
            abort(404)

        data = request.get_json(silent=True) or {}

        if not any(k in data for k in ('question', 'answer', 'category', 'difficulty')):
            abort(400)

        if 'question' in data:
            q.question = data['question']
        if 'answer' in data:
            q.answer = data['answer']
        if 'category' in data:
            q.category = str(data['category'])
        if 'difficulty' in data:
            try:
                q.difficulty = int(data['difficulty'])
            except (TypeError, ValueError):
                abort(400)

        try:
            q.update() 
        except Exception:
            db.session.rollback()
            abort(422)

        return jsonify({
            "success": True,
            "updated": q.id,
            "question": q.format()
        }), 200



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    
    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable content"}), 422

    return app

