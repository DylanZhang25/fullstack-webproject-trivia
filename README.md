# API Development and Documentation Final Project (Trivia App)

## Getting Started
### Pre-requisites and Local Development
Users using this project should already have Python 3.7, pip and node installed on their local machines. Also, this project is built and tested in Windows 11 System.
___
### Project Structure
```
- Trivia API
  - cd0037-API-Development-and-Documentation-project
    - backend/
      - flaskr/
        - __init__.py
      - .env
      - models.py
      - README.md
      - requirements.txt
      - test_flaskr.py
      - trivia.psql
    - frontend/
      - node_modules/
      - public/
      - src
      - package.json
      - package-lock.json
      - README.md
    - CODEOWNERS
    - LICENSE.txt
    - README.md
    - RESUBMISSION NOTE.md
  - venv
    - Include/
    - Lib/
    - Scripts
    - .env
  - .gitignore
  - .git/
```
___
### Backend Setup and Run
#### 1. Set up Python Virtual Environment
* Open Windows Command Prompt at the same level as the project folder
* In the above location, use python 3.7 to create a virtual environment, named venv (random name, here named venv for convenience), using:
```
C:\Users\your_user_name\AppData\Local\Programs\Python\Python37\python.exe -m venv venv
```
Note: `C:\Users\yourUsername\AppData\Local\Programs\Python\Python37` is the default location where you installed your Python 3.7.0 on your Windows.
* In the location at the same level as the virtual environment folder, activate the virtual environment in the terminal using:
```
venv\Scripts\activate
```
#### 2. In the virtual environment, initialize the local folder, and clone the GitHub project to local
#### 3. Installing Dependencies
* In the virtual environment, under the project's backend folder, install the dependency using:
```
pip install -r requirements.txt
```
* To avoid package incompatibility, it is possible to update all packages to the latest version through pip. Here is the versions of my packages:
```
Package            Version
------------------ -------
aniso8601          6.0.0
click              8.1.3
colorama           0.4.6
Flask              2.2.5
Flask-Cors         3.0.7
Flask-RESTful      0.3.7
Flask-SQLAlchemy   3.0.3
greenlet           2.0.2
importlib-metadata 6.6.0
itsdangerous       2.1.2
Jinja2             3.1.2
MarkupSafe         2.1.3
pip                23.1.2
psycopg2           2.9.6
psycopg2-binary    2.8.2
pytz               2019.1
setuptools         39.0.1
six                1.12.0
SQLAlchemy         2.0.16
typing_extensions  4.6.3
Werkzeug           2.2.3
zipp               3.15.0
```
* Using a specific version of the Python interpreter and installed packages in a virtual environment
Create a file named .env in the root directory of the virtual environment (if it does not already exist) and add the following to it:
```
PYTHONPATH=D:\YourPath\Trivia API\venv\Scripts\python.exe
```
#### 4. When the flask entry file is not the default app.py, in the position of your entry file, run the following command in terminal:
```
set FLASK_APP=__init__.py
```
if not, such error "Error: Could not import 'flaskr.app'" will occur.
#### 5. Run Backend
in the folder of the position of `__init__.py`, in the terminal run:
```
flask run --debug --reload 
```
___
### Frontend Setup and Run
#### 1. Installing Dependencies
* Installing Node and NPM
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).
* Installing project dependencies
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```
npm install
```
#### 2. Run Frontend
locate to the frontend folder, in the terminal run:
```
npm start
```
___
### Tests
In SQL Shell (psql) or pgAdmin4, create a database named "trivia_test"
In order to run tests navigate to the backend folder and run the following commands:
```
psql trivia_test < trivia.psql
python test_flaskr.py
```
___
### API Reference
#### Getting Started
* Base URL: the backend app is hosted at the default, http://127.0.0.1:5000.
* Authentication: This application does not require APP keys.

##### Error Handling
Errors are returned as JSON objects following the format below:
```
{
  'success': False,
  'error': 404,
  'Message': 'Not Found'
}
```
When a request fails, the API will return four error types:
* 400
* 404
* 422
* 500

#### Endpoints

`GET '/categories'`
* General:
	* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
	- Request Arguments: None
	- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
* Sample:
	`http://localhost:5000/categories`
* Response format:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
---
`GET '/questions?page=${integer}'`
* General:
	- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
	- Request Arguments: `page` - integer
	- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
* Sample:
	`http://127.0.0.1:5000/questions?page=1`
* Response format:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```
---
`GET '/categories/${id}/questions'`
* General:
	- Fetches questions for a cateogry specified by id request argument
	- Request Arguments: `id` - integer
	- Returns: An object with questions for the specified category, total questions, and current category string
* Sample:
	`http://localhost:5000/categories/2/questions`
* Response format:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```
---
`DELETE '/questions/${id}'`
* General:
	- Deletes a specified question using the id of the question
	- Request Arguments: `id` - integer
	- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
* Sample:
	`http://localhost:5000/questions/100`
---
`POST '/quizzes'`
* General:
	- Sends a post request in order to get the next question
* Sample:
	`http://localhost:5000/quizzes`
- Request Body:

```json
{
    "previous_questions": [21],
    "quiz_category": {"type":"Science","id":"1"}
}
```
- Returns: a single new question object
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```
---
`POST '/questions'`
* General:
	- Sends a post request in order to add a new question
* Sample:
	`http://localhost:5000/questions`
- Request Body:
```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
- Returns: Does not return any new data
---
`POST '/questions/search'`
* General:
	- Sends a post request in order to search for a specific question by search term
* Sample:
	`http://localhost:5000/questions/search`
- Request Body:
```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```