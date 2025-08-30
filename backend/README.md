# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.



GET '/categories'

- Fetches a dictionary of categories where keys are - IDs and values are category names

- Request Arguments: None

- Returns: An object with key categories containing { id: name } pairs

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}

GET '/questions'

- Fetches paginated questions (10 per page) plus category mapping

- Request Arguments (query): page (integer, optional; default 1)

- Returns: questions (list), total_questions (int), categories (map), current_category (null)

{
  "success": true,
  "questions": [
    {
      "id": 12,
      "question": "What is H2O?",
      "answer": "Water",
      "category": "1",
      "difficulty": 1
    }
  ],
  "total_questions": 45,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null
}

POST '/questions' (Search)

- Searches questions by substring (case-insensitive)

- Request Body: { "searchTerm": "<text>" }

- Returns: filtered questions, total_questions, current_category (null)

{
  "success": true,
  "questions": [
    {
      "id": 23,
      "question": "Capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 1
    }
  ],
  "total_questions": 1,
  "current_category": null
}

POST '/questions' (Create)

- Creates a new question

- Request Body:

{
  "question": "Who painted the Mona Lisa?",
  "answer": "Leonardo da Vinci",
  "category": "2",
  "difficulty": 2
}


- Returns: created question info and new total_questions

{
  "success": true,
  "created": 51,
  "question": {
    "id": 51,
    "question": "Who painted the Mona Lisa?",
    "answer": "Leonardo da Vinci",
    "category": "2",
    "difficulty": 2
  },
  "total_questions": 46
}


- DELETE '/questions/<int:question_id>'

- Deletes a question by ID

- Request Arguments (path): question_id (int)

- Returns: the deleted question ID

{
  "success": true,
  "deleted_question": 51
}

GET '/categories/<int:category_id>/questions'

- Fetches paginated questions for a given category

- Request Arguments (path): category_id (int)

- Request Arguments (query): page (integer, optional; default 1)

- Returns: questions list, total_questions for that category, and current_category

{
  "success": true,
  "questions": [
    {
      "id": 10,
      "question": "What planet is red?",
      "answer": "Mars",
      "category": "1",
      "difficulty": 1
    }
  ],
  "total_questions": 8,
  "current_category": 1
}
POST '/quizzes'

- Returns a random question not in previous_questions, optionally filtered by category

- Request Body:

{
  "previous_questions": [10, 12],
  "quiz_category": { "id": 0 }
}


- quiz_category.id = 0 → all categories; otherwise use a real category ID

- Returns (question available):

{
  "success": true,
  "question": {
    "id": 25,
    "question": "Who directed \"Inception\"?",
    "answer": "Christopher Nolan",
    "category": "5",
    "difficulty": 2
  },
  "current_category": 0
}


- Returns (no question available):

{
  "success": true,
  "question": null,
  "current_category": 1
}

- Error Responses (examples)

- 400 Bad Request

{
  "success": false,
  "error": 400,
  "message": "bad request"
}


- 404 Not Found

{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
