import logging
import unittest

from rt_with_exceptions import Runner


class RunnerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            filename="runner_tests.log",
            filemode="w",
            format='%(asctime)s | %(levelname)s: %(message)s',
            level=logging.INFO,
            encoding="utf-8",
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def test_walk(self):
        try:
            runner = Runner("Leonid", -5)
            for _ in range(10):
                runner.walk()
            self.assertEqual(runner.distance, 50)
            logging.info("'test_walk' passed successfully")
        except ValueError:
            logging.warning("Incorrect speed for Runner", exc_info=True)

    def test_run(self):
        try:
            runner = Runner(123)
            for _ in range(10):
                runner.run()
            self.assertEqual(runner.distance, 100)
            logging.info("'test_run' passed successfully")
        except TypeError:
            logging.warning("Incorrect data type for Runner", exc_info=True)

    def test_challenge(self):
        runner_l = Runner("Leonid")
        runner_m = Runner("Max")
        for _ in range(10):
            runner_l.run()
            runner_m.walk()
        self.assertNotEqual(runner_m.distance, runner_l.distance)


if __name__ == "__main__":
    unittest.main()
