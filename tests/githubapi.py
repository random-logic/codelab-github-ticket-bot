import unittest
from ..githubapi import GitHub

class TestGithubApi(unittest.TestCase):
  def test_poll(self):
    api = GitHub()
    api.poll()

if __name__ == '__main__':
  unittest.main()
