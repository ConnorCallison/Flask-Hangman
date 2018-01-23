import unittest
import app


class TestHaangman(unittest.TestCase):
    """
    This testing class will be used to test the
    core logic of the hangman game.
    """

    def test_check_win(self):
    	dict1 = {'b':True,'a':True,'l':True}
    	dict2 = {'b':True,'a':False,'l':True}
    	dict3 = {'b':12,'a':'1qaa','l':True}
    	dict4 = {}

    	self.assertTrue(app.check_win(dict1))
    	self.assertFalse(app.check_win(dict2))
    	self.assertFalse(app.check_win(dict3))
    	self.assertFalse(app.check_win(dict4))

    def test_valid_guess(self):

    	self.assertFalse(app.valid_guess(''))
    	self.assertFalse(app.valid_guess(4))
    	self.assertFalse(app.valid_guess({'guess':'a'}))
    	self.assertTrue(app.valid_guess('a'))
    	self.assertFalse(app.valid_guess('connor'))
    	self.assertFalse(app.valid_guess('9'))
    	self.assertFalse(app.valid_guess(None))

    def test_is_new_guess(self):
    	guesslog = ['a','b','c']

    	self.assertTrue(app.new_guess('d', guesslog))
    	self.assertFalse(app.new_guess('a', guesslog))

    def test_guess_correct(self):

    	dict1 = {'b':False,'a':False,'l':False}

    	self.assertTrue(app.guess_correct('b',dict1))
    	self.assertFalse(app.guess_correct('x',dict1))



if __name__ == '__main__':
	unittest.main()