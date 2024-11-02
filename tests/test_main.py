import unittest
from unittest.mock import patch

from quizcreate import main, QuizCreate

# Using "@patch('builtins.print')" to block print statements from appearing

import yaml
class TestMain(unittest.TestCase):
    with open('quizcreate/example_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    default_quizcreate = QuizCreate(config=config)

    @patch('builtins.input', side_effect=["1", "1", "1"])
    @patch('builtins.print')
    def test_duelist_win(self, mock_print, mock_input):
        self.default_quizcreate.run()
        self.assertEqual(self.default_quizcreate.evaluate_outcomes()['title'], 'Duelist')
    
    @patch('builtins.input', side_effect=["blah-blah-blah.yaml"])
    @patch('builtins.print')
    def test_invalid_config(self, mock_print, mock_input):
        with self.assertRaises(FileNotFoundError):
            main()
    
    def test_no_config(self):
        with self.assertRaises(ValueError):
            quizcreate = QuizCreate()

    @patch('builtins.input', side_effect=["1", "1"])
    @patch('builtins.print')
    def test_tiebreaker(self, mock_print, mock_input):
        with open('tests/tiebreaker.yaml') as f:
            tiebreaker_config = yaml.safe_load(f)
        quizcreate = QuizCreate(config = tiebreaker_config)
        quizcreate.run()
        self.assertEqual(quizcreate.evaluate_outcomes()['title'], "One")

#    @patch('builtins.input', side_effect=["1", "1", "1"])
#    @patch('builtins.print')
#    def test_duelist_win(self, mock_print, mock_input):
#        mock_print.assert_any_call("duelist")


if __name__ == "__main__":
    unittest.main()
