import mysql.connector


class Db:
    """
    Class that initiate the oof_db
    """
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="oof_db")
        self.mycursor = self.db.cursor()
