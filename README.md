# The GrandPy bot project

The grandfather who finds everything !

![grandpybot example](https://image.ibb.co/f0wfkU/grandpybot_example.jpg)

This project is a web application that allows you to chat with a robot. This robot attempts to return the address or location given in the user message, as well as an anecdote of the surroundings.

## Getting Started

You can clone this repository to your local drive and then deploy it to heroku.

### Prerequisites

to use it, you'll need to install:

- python 3.6
- pipenv

### Installing

Run pipenv at the root of the repository to install dependencies.

>**NOTE:** The Javascript file ans CSS file are minified. I used a webpack environnment for frontend developement, and it is not given with this repository. You should recreate your own .js and .css file if you want to modify them.

## Running the tests

I use Pytest for tests. Simply write ```pipenv run python -m pytest``` in your shell, a the root of this repository.

## Deployment

Use heroku for deployment.
You have to create a heroku account and set this project to a new heroku project. Then simply write ```git push heroku master``` to deploy your application.

## Built With

python - back language.  
npm, webpack - Front-end developement.  
material design lite - css/js framework.  
Jquery - Javascript framework.  
flask - python web framework.  
pytest - test framework.  

## Trello Scrum project

**Link to Trello:**
[![link to Trello](https://image.ibb.co/mvESX9/trello.jpg)](https://trello.com/b/SMatrUZV/scrum-board)

## Authors

Mikael Briolet - Initial work - OpenClassroom

## License

There is actually no license for this project.
