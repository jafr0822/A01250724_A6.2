"""Script to run unittest test cases"""

import unittest
import coverage

cov = coverage.Coverage()

cov.start()

import tests.test_cases
suite = unittest.TestLoader().discover("tests")
unittest.TextTestRunner().run(suite)

cov.stop()
cov.html_report(directory="tests/report")
