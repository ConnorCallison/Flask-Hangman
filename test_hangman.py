import unittest
import app


class TestHangman(unittest.TestCase):
    """
    This testing class will be used to test the
    core logic of the hangman game.
    """

    def test_check_win(self):
        dict1 = {'b': True, 'a': True, 'l': True}
        dict2 = {'b': True, 'a': False, 'l': True}
        dict3 = {'b': 12, 'a': '1qaa', 'l': True}
        dict4 = {}

        self.assertTrue(app.check_win(dict1))
        self.assertFalse(app.check_win(dict2))
        self.assertFalse(app.check_win(dict3))
        self.assertFalse(app.check_win(dict4))

    def test_valid_guess(self):

        self.assertFalse(app.valid_guess(''))
        self.assertFalse(app.valid_guess(4))
        self.assertFalse(app.valid_guess({'guess': 'a'}))
        self.assertTrue(app.valid_guess('a'))
        self.assertFalse(app.valid_guess('connor'))
        self.assertFalse(app.valid_guess('9'))
        self.assertFalse(app.valid_guess(None))

    def test_is_new_guess(self):
        guesslog = ['a', 'b', 'c']

        self.assertTrue(app.new_guess('d', guesslog))
        self.assertFalse(app.new_guess('a', guesslog))

    def test_guess_correct(self):

        dict1 = {'b': False, 'a': False, 'l': False}

        self.assertTrue(app.guess_correct('b', dict1))
        self.assertFalse(app.guess_correct('x', dict1))
        self.assertFalse(app.guess_correct(None, dict1))

    def test_create_user(self):
        self.assertTrue(app.create_user('connor'))
        app.remove_user('connor')
        self.assertTrue(app.create_user('c0nn0r'))
        app.remove_user('c0nn0r')
        self.assertFalse(app.create_user(-34))
        self.assertFalse(app.create_user(['first', 'second']))

    def test_is_user(self):
        app.create_user('test_user')
        self.assertTrue(app.is_user('test_user'))
        app.remove_user('test_user')
        self.assertFalse(app.is_user('test_user'))
        self.assertFalse(app.is_user(45))
        self.assertFalse(app.is_user({'user': 123}))
        self.assertFalse(app.is_user(None))

    def test_prime_session(self):
        with app.app.test_request_context():
            app.prime_session()
            self.assertEquals(app.session['guess_log'], [])
            self.assertEquals(app.session['user_incorrect'], 0)
            self.assertIsInstance(app.session['word'], basestring)
            self.assertIsInstance(app.session['word_map'], dict)
            self.assertFalse(app.session.has_key('win'))
            self.assertFalse(app.session.has_key('loss'))

    def test_win(self):
        with app.app.test_request_context():
            app.create_user('test_user')
            app.session['username'] = 'test_user'
            app.session['win'] = True
            app.win()
            user = app.get_user(app.session['username'])
            self.assertEquals(user.wins, 1)
            app.remove_user('test_user')

    def test_game_over(self):
        with app.app.test_request_context():
            app.create_user('test_user')
            app.session['username'] = 'test_user'
            app.session['loss'] = True
            app.session['word'] = 'Tests'
            app.game_over()
            user = app.get_user(app.session['username'])
            self.assertEquals(user.losses, 1)
            app.remove_user('test_user')


if __name__ == '__main__':
    unittest.main()
