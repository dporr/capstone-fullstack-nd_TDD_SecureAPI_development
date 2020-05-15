# Full Stack Nano Degree - Capstone - TDD Secure API Development

## Motivation
Create a functional API with the following requirements
* Maintainable: PEP8 compliant code
* Secure: custom RBAC via Auth0
* Testable: Test-driven development in place for all behaviors, endpoints and access control features
* Documented: All endpoints and roles are documented
* Production-ready: Final code is tested and deployed to Heroku

## Full Stack Trivia Description

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The backend contains a completed Flask and SQLAlchemy server.
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## General environment configutations - Local
Edit the `setup.sh` accordingly and run.
This project makes use of environment variables in order to store sensitive data, ensure you run each command adding an empty space at the begining, before the ```export``` and avoid spaces arround equal sign, this way we avoid storing plaintext secrets on shell history file.
```./setup.sh
```

### Setting up database container - For local testing
First you will need to create a folder that will act as persistent volume for your postgres container
```bash
mkdir -p $HOME/docker/volumes/postgres
```
Then spin up the docker container. the -p setting indicates the port where your DB will be exposed, this should be consistent with the one you include in the app config. (read docker documentation for additional info)
```bash
sudo docker run --rm --name pg-docker -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```
### Creating the database
```python migrations.py db init
python migrations.py db migrate
python migrations.py db upgrade
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development #in case you are testing locally. Don't use this in production
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` and run the application.

## Avaible Endpoints

In order to play the game, a number of operations take place, each one of them belong to a specific endpoint. The available operations are:

- [GET categories](#getCategories)
- [GET questions](#getQuestions1)
- [GET questions (for a specific category)](#getQuestions2)
- [DELETE question](#deleteQuestion)
- [POST question (create question)](#createQuestion)
- [POST question (search question)](#postQuestion)
- [POST quizzes (to play game)](#postQuizzes)
- [PATCh quizzes (to play game)](#patcQuizzes)

***
<h4 id="getCategories"></h4>

> **GET '/categories'**

This endpoint fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

**Request Arguments:**
- *None*

**Returns:** The return should include an success: True message along with the total categories (amount).
Also should include an object with a single key, categories, that contains a object of id & category each of key:value pairs, something like this:

```javascript
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ]}
```
***
<h4 id="getQuestions1"></h4>

> **GET '/questions'**

This endpoint fetches a dictionary of questions available.

**Request Arguments:**
- *None*

**Returns:** The return should include an success: True message along with the amount of questions available, the categories and current_category.
It should also include an object with a single key, questions, that contains a object of id, category, difficulty, answer and question, each of key:value pairs, like this:

```javascript
{
"questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }]
}
```
***
<h4 id="getQuestions2"></h4>

> **GET '/categories/"id"/questions'**

This endpoint fetches a dictionary of questions available for a specific category.

**Request Arguments:**
- *id* (integer) of the category

**Returns:** The return should include an success: True message along with the amount of questions available on that category and current_category.
It should also include an object with a single key, questions, that contains a object of id: question_string key:value pairs.

For example, for category id=1, response should look something like this:

```javascript
{'21' : "Who discovered penicillin?",
'22' : "Hematology is a branch of medicine involving the study of what?",
'20' : "What is the heaviest organ in the human body?",
}
```
***
<h4 id="deleteQuestion"></h4>

> **DELETE '/questions/"id"'**

This endpoint allows you to delete a question, based on its id.

**Request Arguments:**
- *id* (integer) of the question to delete.

**Returns:** An object with a success message, the id of the question deleted and the new amount of questions avaibale.

For example, for question id=1, if we had 21 questions, response should look somethinkg like this:

```javascript
{'success' : True,
'deleted' : 1,
'total_questions' : 20,
}
```
***
<h4 id="createQuestion"></h4>

> **POST '/questions'**

This endpoint allows you to POST a new question.

**Request Arguments:**
- *question* (Text)
- *answer* (Text)
- *difficulty* (integer) 1 to 4.
- *category* (integer) 1 to 6.

**Returns:** An object with a success message, the id of the question created and the new amount of questions avaibale.

For example, for question id=1, if we had 21 questions, response should look somethinkg like this:

```javascript
{'success' : True,
'created' : 25,
'total_questions' : 21,
}
```
***
<h4 id="searchQuestion"></h4>

> **POST '/questions/search'**

This endpoint allows you to search for a question based on a search term, it is case sensitive.

**Request Arguments:**
- *search_term* (Text)

**Returns:** An object with a success message, the questions that match the criteria and the amount of these questions.

For example, for search_term='title', response should look somethinkg like this:

```javascript
{'success' : True,
'questions' : [Question1,Question2],
'total_questions' : 2,
}
```
***
<h4 id="postQuizzes"></h4>

> **POST '/quizzes'**

This endpoint allows you to play the game by getting a random question.

**Request Arguments:**
- *None*

**Returns:** An object with a success message and the new random question: It response should look somethinkg like this:

```javascript
{'success' : True,
'questions' : 'some random question'
}
```
***
<h4 id="updateQuestion"></h4>

> **PATCH '/questions/"id"'**

This endpoint allows you to PATCH an existing question.

**Request Arguments:**
- *question* (Text)
- *answer* (Text)
- *difficulty* (integer) 1 to 4.
- *category* (integer) 1 to 6.

**Returns:** An object with a success message, the id of the question updated.

For example, for question id=1 response should look somethinkg like this:

```javascript
{'success' : True,
'question_id' : 1
}
```
***


## Testing
To run the tests, run
```
python test_app.py
```

# Available Roles
There are 3 roles  and 6 different permissions defined in the Authorization backend for this application
## Permissions:
    ```
    'get:questions': Retrieve a raw list of all questions and allows to use the search endpoint
    'get:categories': List the existent categories
    'get:quizzes': Allows to play a quizzes
    'create:questions': Create new questions under a certain category
    'delete:questions': Delete a question
    'update:questions': Update partially or totally the attributes of a question.
    ```

## Roles
### Player
Can list categories and chose a category for playing. It is the only profile that ca play quizzes.
### QA
Can list and search all questions for reviewing purposes
### Admin
Is the profile in charge of creating, deleting and updating the questions
