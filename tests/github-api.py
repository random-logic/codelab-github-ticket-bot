import unittest
import os


class MyTestCase(unittest.TestCase):
  def test_codelab_repo(self):
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token is None:
      raise Exception("GITHUB_TOKEN environment variable not set")

    # TODO: Add test

if __name__ == '__main__':
  unittest.main()
