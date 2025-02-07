import unittest
from ..camper import Camper

class TestCamper(unittest.TestCase):
  def test_poll(self):
    camper = Camper(repo_name='random-logic/codelab-github-ticket-bot')
    print(camper.read_issues_without_lock_or_first_comment())

if __name__ == '__main__':
  unittest.main()
