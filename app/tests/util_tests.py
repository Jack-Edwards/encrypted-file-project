import unittest
from modules import util

class UtilMethodTests(unittest.TestCase):

    def test_empty_string_is_invalid_filename(self):
        self.assertFalse(util.is_valid_filename(''))

    def test_none_is_invalid_filename(self):
        self.assertFalse(util.is_valid_filename(None))

if __name__ == '__main__':
    unittest.main()
