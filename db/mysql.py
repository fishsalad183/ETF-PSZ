import mysql.connector


class MysqlDAO:
    conf = {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': 'root',
        # 'db': 'nekretnine',
    }

    def __init__(self, database=""):
        if database != "":
            self.conf['db'] = database
        self.conn = self.mysql_connect()
        self.cursor = self.conn.cursor()
        
    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            print(err)
            
    def close(self):
        self.cursor.close()
        self.conn.close()
            
    def create_database(self):
        self.cursor.execute("DROP DATABASE IF EXISTS nekretnine")
        self.cursor.execute("CREATE DATABASE nekretnine")
            
    def create_table(self):
        self.cursor.execute("USE nekretnine")
        self.cursor.execute("DROP TABLE IF EXISTS nekretnine")
        self.cursor.execute("CREATE TABLE nekretnine ("
                            "id INT AUTO_INCREMENT PRIMARY KEY, "
                            "naslov VARCHAR(255), "
                            "tip VARCHAR(255), "
                            "ponuda CHAR(1), "
                            "cena INT "
                            ")")
        self.conn.commit()
        
    def save(self, item):
        self.cursor.execute("INSERT INTO nekretnine (naslov, tip, ponuda, cena)"
                            "VALUES (%s, %s, %s, %s)",
                            (item.get('naslov'),
                             item.get('tip'),
                             item.get('ponuda'),
                             item.get('cena'),
                             )
                            )
        self.conn.commit()
