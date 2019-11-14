import datetime
import sqlite3
import const


def initialize_score_db():
    _execute_dml_query("DROP TABLE IF EXISTS " + const.SCORE_TABLE)
    _execute_dml_query("CREATE TABLE " + const.SCORE_TABLE +
                       " (name TEXT, score INTEGER, date DATE)")


def get_con_cur():
    con = sqlite3.connect(const.DB_FILE)
    cur = con.cursor()
    return con, cur


def close_con_cur(con, cur):
    cur.close()
    con.commit()
    con.close()


def _execute_dml_query(query, args=tuple()):
    con, cur = get_con_cur()
    cur.execute(query, args)
    close_con_cur(con, cur)


def _execute_select_query(query, args=tuple()):
    con, cur = get_con_cur()
    cur.execute(query, args)
    rows = cur.fetchall()
    close_con_cur(con, cur)
    return rows


def add_score(player: str, score: int):
    query = "INSERT INTO " + const.SCORE_TABLE + " VALUES (?, ?, ?)"
    data = player, str(score), str(datetime.date.today())
    _execute_dml_query(query, data)


def get_highscores():
    query = ("SELECT * FROM " + const.SCORE_TABLE + " ORDER BY " +
             "score DESC LIMIT 10")
    return _execute_select_query(query)


def get_scores_near(score: int):
    query = (
        "SELECT * FROM (" +
        "SELECT * FROM " + const.SCORE_TABLE +
        " WHERE score > ? UNION SELECT * FROM " +
        const.SCORE_TABLE + " WHERE score <= ? " +
        ") ORDER BY score DESC LIMIT 10"
    )
    return _execute_select_query(query, [score] * 2)
