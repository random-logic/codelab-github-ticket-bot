import unittest
from ..github.api import GithubAPI

class TestGithubApi(unittest.TestCase):
  def test_poll(self):
    api = GithubAPI()
    api.poll()

if __name__ == '__main__':
  unittest.main()
