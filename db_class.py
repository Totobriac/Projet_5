import mysql.connector


class Db:

    def __init__ (self):        
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="test_off")
        self.mycursor = self.db.cursor() 
        