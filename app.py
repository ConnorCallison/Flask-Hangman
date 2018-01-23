import random
import sys
import string
from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, jsonify, session)
from hangman_states import hangman_states
# from words import words_list
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


@app.route('/', methods=['GET', 'POST'])
def welcome():
    '''
    Index page, allows users to input username, and view previous scores.
    '''

    if request.method == 'GET':
        # Start the session
        prime_session()
        return render_template('index.html', users=get_users())

    elif request.method == 'POST':
        if request.form['username']:
            session['username'] = request.form['username']
            if is_user(session):
                return redirect('/play-hangman')
            else:
                create_user(session)
                return redirect('/play-hangman')
        else:
            flash('Invalid Username.')
            return render_template('index.html', users=get_users())


@app.route('/play-hangman', methods=['GET', 'POST'])
def play_hangman():
    '''
    Main game page, handles all game logic and state management.
    '''
    if request.method == 'POST':

        user_guess = request.form['guess'].lower()

        # If the user guess is valid?
        if valid_guess(user_guess):

            # Is the guess unique?
            if not new_guess(user_guess, session['guess_log']):
                flash('You have already guessed that!')
                return render_game(session)
            else:
                session['guess_log'].append(user_guess)

            # Check if the user has remaining guesses
            if session['user_incorrect'] < 9:

                # Is the guess correct?
                if guess_correct(user_guess, session['word_map']):
                    session['word_map'][user_guess] = True

                    # Have all of the letters been guessed?
                    if check_win(session['word_map']):
                        session['win'] = True
                        return redirect('/win')
                    else:
                        flash('Correct Guess! Guesses remaining: ' +
                              str(10 - session['user_incorrect']))
                        return render_game(session)
                else:
                    session['user_incorrect'] += 1
                    flash('Incorrect Guess. Guesses remaining: ' +
                          str(10 - session['user_incorrect']))
                    return render_game(session)
            else:
                return redirect('/game-over')
        else:
            flash('Invalid guess: must be alphabetical!')
            return render_game(session)
    else:
        return render_game(session)


@app.route('/game-over')
def game_over():
    '''
    Show the user the correct word and prompt to play again.
    '''
    # Add a loss to the users database record.
    db_conn.query(User).filter(User.name == session[
        'username']).update({'losses': User.losses + 1})
    db_conn.commit()
    return render_template('loss.html', word=session['word'])


@app.route('/win')
def win():
    '''
    Congratulate the user on the win and prompt to play again.
    '''
    if session.has_key('win'):
        # Add a win to the users database record.
        db_conn.query(User).filter(User.name == session[
            'username']).update({'wins': User.wins + 1})
        db_conn.commit()
        return render_template('win.html')
    else:
        return redirect('/')

# ------ General helper Functions ------


def guess_correct(guess, word_map):
    '''
    Test if the user guess is in the secret word.
    '''
    if word_map.has_key(guess):
        return True
    else:
        return False


def new_guess(guess, guesslog):
    '''
    Check if the user has already guessed the given letter.
    '''
    if guess in guesslog:
        return False
    else:
        return True


def valid_guess(guess):
    '''
    Ensure that the guess is a string (or unicode) type,
    is not empty, and is alphabetical.
    '''
    if not isinstance(guess, basestring):
        return False
    if guess != '' and guess.isalpha() and len(guess) == 1:
        return True
    else:
        return False


def check_win(word_map):
    '''
    Check if all of the letters in the
    word_map have been guessed.
    '''
    if not word_map:
        return False
    if all(val == True for val in word_map.values()):
        return True


def random_word(filename):
    '''
    Randomly choose a word from the words list.
    The underlying functions will not load the entire
    words list into RAM - reducing usage a significant percentage.
    '''
    with open(filename) as words_file:
        return get_random_line(words_file)


def get_random_line(file):
    '''
    Will select and return a random line from a file.
    Adapted from: http://bit.ly/2n1zvwl
    '''
    file.seek(0, 2)
    last_char = file.tell() - 1  # skipping EOF position with -1
    position = random.randint(0, last_char)

    return get_line(file, position)


def get_line(file, position):
    '''
    Returns a specific line in a file based on a position.
    Adapted from: http://bit.ly/2n1zvwl
    '''
    start_position = position
    while True:
        file.seek(position)
        symbol = file.read(1)
        # get line when reaches \n, and when \n was not the first match
        if symbol == '\n' and file.tell() != start_position + 1:
            return file.readline().rstrip()

        # get symbol + rest of the line when reaches start of file
        elif position == 0:
            return symbol + file.readline().rstrip()

        else:
            position -= 1


def create_user(session):
    '''
    Create the user in the database.
    '''
    newUser = User(name=session['username'],
                   wins=0,
                   losses=0)
    db_conn.add(newUser)
    db_conn.commit()


def is_user(session):
    '''
    Check if a user already exists in the database.
    '''
    if not session:
        return False
    elif not session.has_key('username'):
        return False
    elif not db_conn.query(User)\
            .filter(User.name == session['username']).first():
        return False
    else:
        return True


def get_users():
    '''
    This function will return all user
    objects in the database.
    '''
    return db_conn.query(User).order_by(User.wins.desc()).all()


def render_game(session):
    '''
    This function will render the
    hangman game, getting its current state
    from the session
    '''
    return render_template('play.html',
                           hangman=hangman_states[session['user_incorrect']])


def prime_session():
    '''
    Initializes session variables.
    '''

    session['guess_log'] = []
    session['user_incorrect'] = 0
    session['word'] = random_word('words.txt')
    word_map = {}
    for letter in session['word']:
        word_map[letter.lower()] = False
    session['word_map'] = word_map
    session.pop('win', None)

# ------ Main ------

if __name__ == '__main__':
    random_word('words.txt')
    app.run(host='0.0.0.0', port=8000)
