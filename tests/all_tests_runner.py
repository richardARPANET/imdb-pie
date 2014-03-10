import unittest


def load_tests(loader, tests, pattern):
    """
    Find and load all tests in dir
    """
    suite = unittest.TestSuite()
    for all_tests in unittest.defaultTestLoader.discover('./', pattern='*_test.py'):
        for test in all_tests:
            suite.addTests(test)
    return suite


if __name__ == '__main__':
    unittest.main()
