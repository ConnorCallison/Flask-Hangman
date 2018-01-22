import random
import string
from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, jsonify, session)
from hangman_states import hangman_states
from words import words_list
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User

app = Flask(__name__)
app.secret_key = 'PQ36N93Ste'

engine = create_engine('sqlite:///scores.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_conn = DBSession()

#  ------ App Routes ------

# Index page, allows users to input username, and view previous scores.
@app.route('/', methods=['GET','POST'])
def welcome():

    if request.method == 'GET':
        # Start the session
        prime_session()
        return render_template('index.html', users=db_conn.query(User).order_by(User.wins.desc()).all())

    elif request.method == 'POST':
        if request.form['username']:
            session['username'] = request.form['username']
            if isUser(session):
                return redirect('/play-hangman')
            else:
                createUser(session)
                return redirect('/play-hangman')
        else:
            flash("Invalid Username.")
            return render_template('index.html', users=db_conn.query(User).order_by(User.wins.desc()).all())

    
# Main game page, handles all game logic and state management.
@app.route('/play-hangman', methods=['GET','POST'])
def play_hangman():
    if request.method == "POST":

        user_guess = request.form['guess'].lower()

        # If the user guess is valid?
        if user_guess != '' and user_guess.isalpha():

            # Is the guess unique?
            if user_guess in session['guess_log']:
                flash("You have already guessed that!")
                return render_template('play.html', hangman=hangman_states[session['user_incorrect']])
            else:
                session['guess_log'].append(user_guess)

            # Check if the user has remaining guesses
            if session['user_incorrect'] < 9:

                # Is the guess correct?
                if session['word_map'].has_key(user_guess):
                    session['word_map'][user_guess] = True

                    # Have all of the letters been guessed?
                    if all(value == True for value in session['word_map'].values()):
                        return redirect('/win')
                    else:
                        flash("Correct Guess! Guesses remaining: " + str(10 - session['user_incorrect']))
                        return render_template('play.html', hangman=hangman_states[session['user_incorrect']])
                else:
                    session['user_incorrect']+=1
                    flash("Incorrect Guess. Guesses remaining: " + str(10 - session['user_incorrect']) )
                    return render_template('play.html', hangman=hangman_states[session['user_incorrect']])
            else:
                return redirect('/game-over')
        else:
            flash("Invalid guess: must be alphabetical!")
            return render_template('play.html', hangman=hangman_states[session['user_incorrect']])
    else:
        return render_template('play.html', hangman=hangman_states[session['user_incorrect']])

# Show the user the correct word and prompt to play again.
@app.route('/game-over')
def game_over():
    db_conn.query(User).filter(User.name == session['username']).update({'losses': User.losses + 1})
    db_conn.commit()
    return render_template('loss.html', word = session['word'])

# Congratulate the user on the win and prompt to play again. 
@app.route('/win')
def win():
    db_conn.query(User).filter(User.name == session['username']).update({'wins': User.wins + 1})
    db_conn.commit()
    return render_template('win.html')

# ------ General helper Functions ------

# Create the user in the database.
def createUser(session):
    newUser = User(name=session['username'],
                   wins=0,
                   losses=0)
    db_conn.add(newUser)
    db_conn.commit()

# Check if a user already exists.
def isUser(session):
    if not session:
        return False
    elif not session.has_key('username'):
        return False
    elif not db_conn.query(User).filter(User.name == session['username']).first():
        return False
    else:
        return True

# Initialize the session variables.
def prime_session():
    session['guess_log'] = []
    session['user_incorrect'] = 0
    session['word'] = random.choice(words_list)
    word_map = {}
    for letter in session['word']:
        word_map[letter.lower()] = False
    session['word_map'] = word_map

# ------ Main ------

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)