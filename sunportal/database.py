import sqlite3


class DatabaseHandler:
    """Database class for handling database calls."""

    def __init__(self, database_file, multiplier):
        self.db = sqlite3.connect(database_file)
        self.multiplier = multiplier

    def get_data(self, from_time, to_time):
        pass

    def get_current_total(self):
        c = self.db.cursor()
        query = '''SELECT ETotal
                FROM SpotData
                WHERE TimeStamp = (
                    SELECT MAX(TimeStamp) 
                    FROM SpotData
                );'''
        return c.execute(query).fetchall()[0][0]

    def get_current_day(self):
        c = self.db.cursor()
        query = '''SELECT EToday
                        FROM SpotData
                        WHERE TimeStamp = (
                            SELECT MAX(TimeStamp) 
                            FROM SpotData
                        );'''
        return c.execute(query).fetchall()[0][0]

    def get_power_last_24h(self):
        c = self.db.cursor()
        query = '''SELECT TimeStamp, Power 
                FROM DayData 
                WHERE TimeStamp >= (
                    SELECT (MAX(TimeStamp)-86400) 
                    FROM DayData
                );'''
        data = list()
        for time, power in c.execute(query):
            data.append(dict({"time": time, "power": power}))
        return data

    def get_current_co2(self):
        current_total = self.get_current_total()
        return (current_total*self.multiplier)/1000

    def get_last_update(self):
        c = self.db.cursor()
        query = '''SELECT MAX(TimeStamp) AS TimeStamp 
                FROM SpotData;'''
        return c.execute(query).fetchall()[0][0]

    def close(self):
        self.db.close()
