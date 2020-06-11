# Trivia API
Trivia api is a web application that allows people to hold trivia on a regular basis using a webpage to manage the trivia app and play the game.

##The app allows one to:

Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
Delete questions.
Add questions and require that they include question and answer text.
Search for questions based on a text query string.
Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
# Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

## Virtual Enviornment
Working within a virtual environment is recommended.

## PIP Dependencies
navigate to the /backend directory and run:

## pip install -r requirements.txt
This will install all of the required packages in the requirements.txt file.

## Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

psql trivia < trivia.psql
Running the server
From within the backend directory

#### To run the server, execute:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

# Testing
### To run the tests, run

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

## Frontend Dependencies
This project uses NPM to manage software dependencies. from the frontend directory run:

npm install
- Running the Frontend in Dev Mode
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

npm start

## API Reference
Getting Started
Backend Base URL: http://127.0.0.1:5000/
Frontend Base URL: http://127.0.0.1:3000/
Authentication: Authentication or API keys are not used in the project yet.

## Error Handling
Errors are returned in the following json format:
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
      
## The error codes currently returned are:
400 – bad request
404 – resource not found
422 – unprocessable

#### Endpoints

- GET /categories

** Returns all the categories.**

    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    }
    
- GET /questions

** Returns all questions **
questions are in a paginated.
pages could be requested by a query string

        {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 19
}

- DELETE /questions/<int:id>

**Deletes a question by id form the url parameter.**

        {
          "success": "True",
          "message": "Question successfully deleted"
        }
        
- POST /questions

** Creates a new question based on a payload.**

{ 
"question": "Frankie Fredericks represented which African country in athletics?", 
"answer": "Namibia",
"difficulty": 3,
"category": "6" 
}'

{
  "message": "Question successfully created!",
  "success": true
}
- POST /questions/search

** returns questions that has the search substring ** 
 '{"searchTerm": "Anne Rice"}'

{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 20
}

- GET /categories/int:<category_id>/questions

** Gets questions by category using the id from the url parameter.**
 
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}

- POST /quizzes

** Takes the category and previous questions in the request.**
Return random question not in previous questions.

{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
} 

