import sqlite3


class DatabaseHandler:
    """Database class for handling database calls."""

    def __init__(self, database_file, multiplier):
        """
        Initialize the DatabaseHandler.

        :param database_file: the location of the database file
        :param multiplier: the CO2 multiplier
        """
        self.db = sqlite3.connect(database_file)
        self.multiplier = multiplier

    def get_current_total(self):
        """
        Get the current total energy generated.

        :return: the total current energy generated
        """
        c = self.db.cursor()
        query = """SELECT ETotal
                FROM SpotData
                WHERE TimeStamp = (
                    SELECT MAX(TimeStamp) 
                    FROM SpotData
                );"""
        return c.execute(query).fetchall()[0][0]

    def get_current_day(self):
        """
        Get the current total energy generated for today.

        :return: the total current energy generated for today.
        """
        c = self.db.cursor()
        query = """SELECT EToday
                        FROM SpotData
                        WHERE TimeStamp = (
                            SELECT MAX(TimeStamp) 
                            FROM SpotData
                        );"""
        return c.execute(query).fetchall()[0][0]

    def get_power_last_24h(self):
        """
        Get the last 24 hours of data from the database.

        :return: the last 24 hours of data from the database in the following format:
        [
            {
                "time": [time],
                "power": [power]
            },
            {
                "time": [time],
                "power": [power],
            },
            ...
        ]
        """
        c = self.db.cursor()
        query = """SELECT TimeStamp, Power 
                FROM DayData 
                WHERE TimeStamp >= (
                    SELECT (MAX(TimeStamp)-86400) 
                    FROM DayData
                );"""
        data = list()
        for time, power in c.execute(query):
            data.append(dict({"time": time, "power": power}))
        return data

    def get_current_co2(self):
        """
        Get the current total co2 avoided.

        :return: the current total co2 avoided
        """
        current_total = self.get_current_total()
        return (current_total * self.multiplier) / 1000

    def get_last_update(self):
        """
        Get the last update time.

        :return: the last update time
        """
        c = self.db.cursor()
        query = """SELECT MAX(TimeStamp) AS TimeStamp 
                FROM SpotData;"""
        return c.execute(query).fetchall()[0][0]

    def close(self):
        """
        Close the database connection.

        :return: None
        """
        self.db.close()
