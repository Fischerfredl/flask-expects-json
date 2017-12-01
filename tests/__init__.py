import unittest


def loader():
    return unittest.TestLoader().discover('tests', pattern='test*.py')


def test_suite():
    return unittest.TestSuite(loader())


def run():
    return unittest.TextTestRunner(verbosity=2).run(loader())