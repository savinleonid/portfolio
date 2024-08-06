from runner_and_tournament import *
import unittest


class TournamentTest(unittest.TestCase):
    def setUp(self):
        self.runner1 = Runner("Усэйн", 10)
        self.runner2 = Runner("Андрей", 9)
        self.runner3 = Runner("Ник", 3)

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}
        cls.counter = 0

    @classmethod
    def tearDownClass(cls):
        for res in cls.all_results.values():
            print(res)

    def test_first_run(self):
        results = Tournament(90, self.runner1, self.runner3).start()
        self.assertTrue(results.get(len(results.keys())).name == "Ник")
        for idx, runner in results.items():
            results[idx] = runner.name
        self.all_results[TournamentTest.counter] = results
        TournamentTest.counter += 1

    def test_second_run(self):
        results = Tournament(90, self.runner2, self.runner3).start()
        self.assertTrue(results.get(len(results.keys())).name == "Ник")
        for idx, runner in results.items():
            results[idx] = runner.name
        self.all_results[TournamentTest.counter] = results
        TournamentTest.counter += 1

    def test_third_run(self):
        results = Tournament(90, self.runner1, self.runner2, self.runner3).start()
        self.assertTrue(results.get(len(results.keys())).name == "Ник")
        for idx, runner in results.items():
            results[idx] = runner.name
        self.all_results[TournamentTest.counter] = results
        TournamentTest.counter += 1


if __name__ == "__main__":
    unittest.main()
