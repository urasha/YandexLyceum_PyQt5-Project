import sqlite3


class Recording_and_analysis_of_points:
    def __init__(self):
        self.average = 0
        self.max = 0

    def open(self):
        self.bd = sqlite3.connect("../design/scoreDB.db")
        self.cur = self.bd.cursor()

    def max_score(self):
        req = 'SELECT MAX(score) FROM all_score'
        result = self.bd.execute(req)
        return result.fetchone()[0]

    def averages_score(self):
        req = 'select avg(score) from all_score'
        result = self.bd.execute(req)
        return result.fetchone()[0]

    def recording_score(self, score):
        req = f"""INSERT INTO all_score(score) VALUES({score})"""
        self.bd.execute(req)

    def close(self):
        self.bd.commit()
        self.bd.close()

