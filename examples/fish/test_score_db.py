import unittest
from fish import ScoreBoardDB
import time
import datetime
from functools import partial

class TestScoreDB(unittest.TestCase):

    score_board_db = ScoreBoardDB("test.db")    

    def create_dataset(self, size):
        query = "INSERT INTO " + ScoreBoardDB.SCORE_TABLE + " VALUES (?, ?, ?)"
        data = []
        today = str(datetime.date.today())
        for i in range(size):
            data.append(("player" + str(i), i, today))
        con, cur = self.score_board_db.get_con_cur()
        cur.executemany(query, data)
        self.score_board_db.close_con_cur(con, cur)

    def _get_scores_near_time_test_helper(self, size: int):
        self.create_dataset(size)
        half_size = size // 2
        dad = timed_function(partial(ScoreBoardDB.get_scores_near, half_size))
        #joe = timed_function(partial(ScoreBoardDB.get_scores_near_2,
                                     "player" + str(half_size) , half_size))
        #self.assertLess(dad, joe)
    
    def test_dad_small_dataset(self):
        self._get_scores_near_time_test_helper(1000)

    def test_dad_medium_dataset(self):
        self._get_scores_near_time_test_helper(10000)

    def test_dad_large_dataset(self):
        self._get_scores_near_time_test_helper(100000)
    
    def test_dad_huge_dataset(self):
        self._get_scores_near_time_test_helper(1000000)
    
    def test_joe_memory(self):
        size = 10000000
        self.create_dataset(size)
        half_size = size // 2
        #ScoreBoardDB.get_scores_near_2("player" + str(half_size) , half_size)

    """    
    @staticmethod
    def get_scores_near_2(name: str, score: int):
        query = (
            "SELECT * FROM " + ScoreBoardDB.SCORE_TABLE +
            " ORDER BY score DESC"
        )
        rows = ScoreBoardDB.execute_select_query(query)
        end = len(rows)
        if rows:
            score_idx = rows.index((name, score, str(datetime.date.today())))
        else:
            return rows
        if score_idx + 4 < end:
            end = score_idx + 4
        return rows[score_idx - 5 : end]
    """


def timed_function(func) -> int:
    start = time.time()
    func()
    end = time.time()
    return end - start

if __name__ == "__main__":
    unittest.main(verbosity=True)