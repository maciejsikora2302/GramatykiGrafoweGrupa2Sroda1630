import unittest

# show that tests are actually run
# TODO: remove when actual tests for productions are added
class Trivial_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_true(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
