import unittest
from ..model import Model

class MyTestCase(unittest.TestCase):
  def test_polling(self):
    model = Model()
    model.add_chunk_to_database("I like apples")
    model.add_chunk_to_database("I don't like oranges")
    model.add_chunk_to_database("I am ok with peaches")
    results = model.retrieve("What do I think about peaches?")

    self.assertEqual(results[0][0], "I am ok with peaches")

if __name__ == '__main__':
  unittest.main()
