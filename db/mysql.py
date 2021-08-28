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
                            "cena INT, "
                            "grad VARCHAR(255), "
                            "deo_grada VARCHAR(255), "
                            "kvadratura INT, "
                            "stanje VARCHAR(255), "
                            "godina_izgradnje INT, "
                            "povrsina_zemljista INT, "
                            "sprat INT, "
                            "spratnost INT, "
                            "opremljenost VARCHAR(255), "
                            "uknjizeno BOOLEAN, "
                            "grejanje VARCHAR(255), "
                            "broj_soba DECIMAL(3, 1), "
                            "broj_kupatila INT, "
                            "parking BOOLEAN, "
                            "lift BOOLEAN, "
                            "terasa BOOLEAN "
                            ")")
        self.conn.commit()
        
    def save(self, item):
        self.cursor.execute("INSERT INTO nekretnine ("
                            "naslov, tip, ponuda, cena, grad, deo_grada, kvadratura, stanje, godina_izgradnje, povrsina_zemljista, sprat, spratnost, opremljenost, uknjizeno, grejanje, broj_soba, broj_kupatila, parking, lift, terasa"
                            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (item.get('naslov'),
                             item.get('tip'),
                             item.get('ponuda'),
                             item.get('cena'),
                             item.get('grad'),
                             item.get('deo_grada'),
                             item.get('kvadratura'),
                             item.get('stanje'),
                             item.get('godina_izgradnje'),
                             item.get('povrsina_zemljista'),
                             item.get('sprat'),
                             item.get('spratnost'),
                             item.get('opremljenost'),
                             item.get('uknjizeno'),
                             item.get('grejanje'),
                             item.get('broj_soba'),
                             item.get('broj_kupatila'),
                             item.get('parking'),
                             item.get('lift'),
                             item.get('terasa'),
                             )
                            )
        self.conn.commit()
