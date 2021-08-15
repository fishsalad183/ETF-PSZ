import mysql.connector


class MysqlDAO:
    conf = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        # 'db': 'nekretnine',
    }
    
    def __init__(self):
        self.con = self.mysql_connect()
        self.cursor = self.con.cursor()
        
    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            print(err)
            
    def create_database(self):
        self.cursor.execute("DROP DATABASE IF EXISTS nekretnine")
        self.cursor.execute("CREATE DATABASE nekretnine")
            
    def create_table(self):
        self.cursor.execute("USE nekretnine")
        self.cursor.execute("DROP TABLE IF EXISTS nekretnine")
        self.cursor.execute("CREATE TABLE nekretnine ("
                         "id INT AUTO_INCREMENT PRIMARY KEY, "
                         "naslov VARCHAR(255), "
                         "cena INT "
                         ")")