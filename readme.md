# Flask-hangman

![alt text](https://i.imgur.com/krj6Cdm.png "Flask Hangman")

## Dependencies

> Python 2.7
> pip

## Getting started

1. Clone this repository:

2. Run the following command within the flask-hangman directory: 
`pip install -r requirements.txt`

3. Run the following command: `gunicorn -w 2 app:app`

4. Visit http://localhost:8000/

### Misc.

The words list (`words.txt`) contains words that would be more commonly known
and reasonably guessable. However all words less than four character long have been removed.
Source: https://github.com/Xethron/Hangman/blob/master/words.txt
