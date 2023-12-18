import unittest
from main import read_file, part2


class TestDay14Part2(unittest.TestCase):
    def test_cycles(self):
        platform = read_file("2023/14/testdata/1.txt")

        expected_files = [
            "2023/14/testdata/1-cycle.txt",
            "2023/14/testdata/2-cycle.txt",
            "2023/14/testdata/3-cycle.txt",
        ]

        for expected_file in expected_files:
            expected = read_file(expected_file)
            platform.cycle()
            for i, row in enumerate(platform.positions):
                for j, entry in enumerate(row):
                    self.assertEqual(entry, expected.positions[i][j])

    def test_part2(self):
        platform = read_file("2023/14/testdata/1.txt")
        retval = part2(platform)
        self.assertEqual(retval, 64)


if __name__ == "__main__":
    unittest.main()
