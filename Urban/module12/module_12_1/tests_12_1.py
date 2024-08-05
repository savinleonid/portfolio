from runner import Runner
import unittest


class RunnerTest(unittest.TestCase):
    def test_walk(self):
        runner = Runner("Leonid")
        for _ in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)

    def test_run(self):
        runner = Runner("Leonid")
        for _ in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    def test_challenge(self):
        runner_l = Runner("Leonid")
        runner_m = Runner("Max")
        for _ in range(10):
            runner_l.run()
            runner_m.walk()
        self.assertNotEqual(runner_m.distance, runner_l.distance)


if __name__ == "__main__":
    unittest.main()

