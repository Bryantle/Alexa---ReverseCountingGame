from flask import Flask, render_template
from flask_ask import Ask, question, session, statement
import json
import requests
import time
import unidecode
import logging
from random import randint


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@app.route('/') #app cause we are referencing flask
def homepage():
    return ("Flask page for the flask ask")

@ask.launch
def new_game():
    welcome_message = render_template('welcome')
    return question(welcome_message)

@ask.intent("YesIntent")
def next_round():
    numbers = [randint(0,9) for _ in range(3)]
    round_message = redner_template('round', numbers = numbers)
    session.attributes['numbers'] = numbers[::-1]
    return question(round_message)

@ask.intent("AnswerIntent", convert = {'first': int, 'second':int, 'third':int})
def answer(first,second,third):
    winning_numbers = session.attributes['numbers']
    if [first,second,third] == winning_numbers:
        message = render_template('win')
    else:
        message = render_template('lose')
    return statement(message)

if __name__ == '__main__':
    app.run(debug = True)
