import unittest
from Urban.module12.module_12_3.tests.tests_12_1 import RunnerTest
from Urban.module12.module_12_3.tests.tests_12_2 import TournamentTest

suit = unittest.TestSuite()
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suit)
