import mysql.connector


class MysqlDAO:
    conf = {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': 'root',
        # 'db': 'vozila',
        # 'db': 'nekretnine',
    }
    dump_file = "db\Dump20220530.sql"

    def __init__(self, database=""):
        if database != "":
            self.conf['db'] = database
        self.conn = self.mysql_connect()
        self.cursor = self.conn.cursor(dictionary=True)

    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            print(err)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def import_database_from_dump(self):
        with open(self.dump_file, encoding='utf-8') as f:
            # Because the insert statement in the dump file is only one line
            self.cursor.execute('SET GLOBAL max_allowed_packet=67108864')
            self.conn.commit()
            self.cursor.close()
            self.cursor = self.conn.cursor(dictionary=True)

            self.cursor.execute(f.read(), multi=True)

    def create_database(self):
        self.cursor.execute("DROP DATABASE IF EXISTS vozila")
        self.cursor.execute("CREATE DATABASE vozila")
        self.conn.commit()

    def create_table(self):
        self.cursor.execute("USE vozila")
        self.cursor.execute("DROP TABLE IF EXISTS vozila")
        self.cursor.execute("CREATE TABLE vozila ("
                            "id INT AUTO_INCREMENT PRIMARY KEY, "
                            "url VARCHAR(255), "
                            "naslov VARCHAR(255), "
                            "cena VARCHAR(255), "
                            "stanje VARCHAR(255), "
                            "marka VARCHAR(255), "
                            "model VARCHAR(255), "
                            "godiste INT, "
                            "kilometraza INT, "
                            "karoserija VARCHAR(255), "
                            "gorivo VARCHAR(255), "
                            "kubikaza INT, "
                            "snaga VARCHAR(255), "
                            "menjac VARCHAR(255), "
                            "vrata VARCHAR(255), "
                            "boja VARCHAR(255), "
                            "lokacija_prodavca VARCHAR(255) "
                            ")")
        self.conn.commit()

    def save_vozilo(self, item):
        self.cursor.execute("INSERT INTO vozila ("
                            "url, naslov, cena, stanje, marka, model, godiste, kilometraza, karoserija, gorivo, kubikaza, snaga, menjac, vrata, boja, lokacija_prodavca"
                            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (item.get('url'),
                             item.get('naslov'),
                             item.get('cena'),
                             item.get('stanje'),
                             item.get('marka'),
                             item.get('model'),
                             item.get('godiste'),
                             item.get('kilometraza'),
                             item.get('karoserija'),
                             item.get('gorivo'),
                             item.get('kubikaza'),
                             item.get('snaga'),
                             item.get('menjac'),
                             item.get('vrata'),
                             item.get('boja'),
                             item.get('lokacija_prodavca'),
                             )
                            )
        self.conn.commit()

    # def prodaja_iznajmljivanje(self):
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE ponuda = 'P'")
    #     prodaja_count = self.cursor.fetchall()
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE ponuda = 'I'")
    #     iznajmljivanje_count = self.cursor.fetchall()
    #     return {
    #         "prodaja": prodaja_count,
    #         "iznajmljivanje": iznajmljivanje_count,
    #     }

    # def prodaja_po_gradovima(self):
    #     self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND tip = 'stan' GROUP BY grad ORDER BY broj DESC")
    #     stanovi = self.cursor.fetchall()
        
    #     self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND tip = 'kuca' GROUP BY grad ORDER BY broj DESC")
    #     kuce = self.cursor.fetchall()
        
    #     self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND (tip = 'stan' OR tip = 'kuca') GROUP BY grad ORDER BY broj DESC")
    #     stanovi_i_kuce = self.cursor.fetchall()
        
    #     return {
    #         'stanovi': stanovi,
    #         'kuce': kuce,
    #         'stanovi_i_kuce': stanovi_i_kuce,
    #     }
    
    # def uknjizenost(self):
    #     uknj = {}
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND uknjizeno IS TRUE")
    #     uknj['stanovi_uknjizeno'] = self.cursor.fetchall()
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND uknjizeno IS NOT TRUE")
    #     uknj['stanovi_neuknjizeno'] = self.cursor.fetchall()
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'kuca' AND uknjizeno IS TRUE")
    #     uknj['kuce_uknjizeno'] = self.cursor.fetchall()
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'kuca' AND uknjizeno IS NOT TRUE")
    #     uknj['kuce_neuknjizeno'] = self.cursor.fetchall()
    #     return uknj
        
    # def najskuplje(self):
    #     self.cursor.execute("SELECT id, naslov, cena, grad, kvadratura, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE ponuda = 'P' and tip = 'stan' ORDER BY cena DESC LIMIT 30")
    #     najskuplji_stanovi = self.cursor.fetchall()
    #     self.cursor.execute("SELECT id, naslov, cena, grad, kvadratura, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE ponuda = 'P' and tip = 'kuca' ORDER BY cena DESC LIMIT 30")
    #     najskuplje_kuce = self.cursor.fetchall()
    #     return {
    #         'najskuplji_stanovi': najskuplji_stanovi,
    #         'najskuplje_kuce': najskuplje_kuce,
    #     }
        
    # def najvece(self):
    #     self.cursor.execute("SELECT id, naslov, kvadratura, ponuda, cena, grad, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'stan' ORDER BY kvadratura DESC LIMIT 100")
    #     najveci_stanovi = self.cursor.fetchall()
    #     self.cursor.execute("SELECT id, naslov, kvadratura, ponuda, cena, grad, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'kuca' ORDER BY kvadratura DESC LIMIT 100")
    #     najvece_kuce = self.cursor.fetchall()
    #     return {
    #         'najveci_stanovi': najveci_stanovi,
    #         'najvece_kuce': najvece_kuce,
    #     }

    # def cene_2020(self):
    #     self.cursor.execute("SELECT id, cena, naslov, grad, kvadratura FROM nekretnine WHERE godina_izgradnje = '2020' AND ponuda = 'P' ORDER BY cena DESC")
    #     prodaja = self.cursor.fetchall()
    #     self.cursor.execute("SELECT id, cena, naslov, grad, kvadratura FROM nekretnine WHERE godina_izgradnje = '2020' AND ponuda = 'I' ORDER BY cena DESC")
    #     izdavanje = self.cursor.fetchall()
    #     return {
    #         'prodaja': prodaja,
    #         'izdavanje': izdavanje,
    #     }
        
    # def top_broj_soba(self):
    #     self.cursor.execute("SELECT id, broj_soba, tip, naslov, cena, grad, kvadratura, broj_soba, broj_kupatila FROM nekretnine ORDER BY broj_soba DESC LIMIT 30")
    #     return self.cursor.fetchall()
        
    # def top_kvadratura_stanovi(self):
    #     self.cursor.execute("SELECT id, kvadratura, naslov, cena, grad, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'stan' ORDER BY kvadratura DESC LIMIT 30")
    #     return self.cursor.fetchall()
    
    # def top_povrsina_zemljista(self):
    #     self.cursor.execute("SELECT id, povrsina_zemljista, naslov, cena, kvadratura, grad FROM nekretnine ORDER BY povrsina_zemljista DESC LIMIT 30")
    #     return self.cursor.fetchall()

    # def top_delovi_beograda(self):
    #     self.cursor.execute("SELECT deo_grada, COUNT(*) AS broj_nekretnina FROM nekretnine WHERE grad = 'Beograd' GROUP BY deo_grada ORDER BY broj_nekretnina DESC LIMIT 10")
    #     return self.cursor.fetchall()
    
    # def broj_nekretnina_u_beogradu(self):
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE grad = 'beograd'")
    #     return self.cursor.fetchone()['broj']
    
    # def kategorije_kvadrature(self):
    #     kategorije = {}
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura <= 35")
    #     kategorije['do_35'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 35 AND kvadratura <= 50")
    #     kategorije['36-50'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 51 AND kvadratura <= 65")
    #     kategorije['51-65'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 66 AND kvadratura <= 80")
    #     kategorije['66-80'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 81 AND kvadratura <= 95")
    #     kategorije['81-95'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 96 AND kvadratura <= 110")
    #     kategorije['96-110'] = self.cursor.fetchone()['broj']
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 110")
    #     kategorije['od_111'] = self.cursor.fetchone()['broj']
    #     return kategorije
    
    # def broj_stanova_za_prodaju(self):
    #     self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P'")
    #     return self.cursor.fetchone()['broj']
        
    # def nekretnine_po_dekadama(self):
    #     nekretnine = {}
    #     prepared_statement = "SELECT COUNT(*) AS broj FROM nekretnine WHERE godina_izgradnje >= %s AND godina_izgradnje <= %s"
    #     dekade = [(1951, 1960), (1961, 1970), (1971, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2020)]
    #     for d in dekade:
    #         self.cursor.execute(prepared_statement, d)
    #         nekretnine[str(d)] = self.cursor.fetchone()['broj']
    #     return nekretnine


# class MysqlDAO:
#     conf = {
#         'host': 'localhost',
#         'port': '3306',
#         'user': 'root',
#         'password': 'root',
#         # 'db': 'nekretnine',
#     }
#     dump_file = "db\Dump20210901.sql"

#     def __init__(self, database=""):
#         if database != "":
#             self.conf['db'] = database
#         self.conn = self.mysql_connect()
#         self.cursor = self.conn.cursor(dictionary=True)

#     def mysql_connect(self):
#         try:
#             return mysql.connector.connect(**self.conf)
#         except mysql.connector.Error as err:
#             print(err)

#     def close(self):
#         self.cursor.close()
#         self.conn.close()

#     def import_database_from_dump(self):
#         with open(self.dump_file, encoding='utf-8') as f:
#             # Because the insert statement in the dump file is only one line
#             self.cursor.execute('SET GLOBAL max_allowed_packet=67108864')
#             self.conn.commit()
#             self.cursor.close()
#             self.cursor = self.conn.cursor(dictionary=True)

#             self.cursor.execute(f.read(), multi=True)

#     def create_database(self):
#         self.cursor.execute("DROP DATABASE IF EXISTS nekretnine")
#         self.cursor.execute("CREATE DATABASE nekretnine")
#         self.conn.commit()

#     def create_table(self):
#         self.cursor.execute("USE nekretnine")
#         self.cursor.execute("DROP TABLE IF EXISTS nekretnine")
#         self.cursor.execute("CREATE TABLE nekretnine ("
#                             "id INT AUTO_INCREMENT PRIMARY KEY, "
#                             "url VARCHAR(255), "
#                             "naslov VARCHAR(255), "
#                             "tip VARCHAR(255), "
#                             "ponuda CHAR(1), "
#                             "cena INT, "
#                             "grad VARCHAR(255), "
#                             "deo_grada VARCHAR(255), "
#                             "kvadratura DECIMAL(10, 2), "
#                             "stanje VARCHAR(255), "
#                             "godina_izgradnje INT, "
#                             "povrsina_zemljista INT, "
#                             "sprat VARCHAR(255), "
#                             "spratnost INT, "
#                             "opremljenost VARCHAR(255), "
#                             "uknjizeno BOOLEAN, "
#                             "grejanje VARCHAR(255), "
#                             "broj_soba DECIMAL(3, 1), "
#                             "broj_kupatila INT, "
#                             "parking BOOLEAN, "
#                             "lift BOOLEAN, "
#                             "terasa BOOLEAN "
#                             ")")
#         self.conn.commit()

#     def save_nekretnina(self, item):
#         self.cursor.execute("INSERT INTO nekretnine ("
#                             "url, naslov, tip, ponuda, cena, grad, deo_grada, kvadratura, stanje, godina_izgradnje, povrsina_zemljista, sprat, spratnost, opremljenost, uknjizeno, grejanje, broj_soba, broj_kupatila, parking, lift, terasa"
#                             ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                             (item.get('url'),
#                              item.get('naslov'),
#                              item.get('tip'),
#                              item.get('ponuda'),
#                              item.get('cena'),
#                              item.get('grad'),
#                              item.get('deo_grada'),
#                              item.get('kvadratura'),
#                              item.get('stanje'),
#                              item.get('godina_izgradnje'),
#                              item.get('povrsina_zemljista'),
#                              item.get('sprat'),
#                              item.get('spratnost'),
#                              item.get('opremljenost'),
#                              item.get('uknjizeno'),
#                              item.get('grejanje'),
#                              item.get('broj_soba'),
#                              item.get('broj_kupatila'),
#                              item.get('parking'),
#                              item.get('lift'),
#                              item.get('terasa'),
#                              )
#                             )
#         self.conn.commit()

#     def prodaja_iznajmljivanje(self):
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE ponuda = 'P'")
#         prodaja_count = self.cursor.fetchall()
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE ponuda = 'I'")
#         iznajmljivanje_count = self.cursor.fetchall()
#         return {
#             "prodaja": prodaja_count,
#             "iznajmljivanje": iznajmljivanje_count,
#         }

#     def prodaja_po_gradovima(self):
#         self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND tip = 'stan' GROUP BY grad ORDER BY broj DESC")
#         stanovi = self.cursor.fetchall()
        
#         self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND tip = 'kuca' GROUP BY grad ORDER BY broj DESC")
#         kuce = self.cursor.fetchall()
        
#         self.cursor.execute("SELECT COUNT(*) AS broj, grad FROM nekretnine WHERE ponuda = 'P' AND (tip = 'stan' OR tip = 'kuca') GROUP BY grad ORDER BY broj DESC")
#         stanovi_i_kuce = self.cursor.fetchall()
        
#         return {
#             'stanovi': stanovi,
#             'kuce': kuce,
#             'stanovi_i_kuce': stanovi_i_kuce,
#         }
    
#     def uknjizenost(self):
#         uknj = {}
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND uknjizeno IS TRUE")
#         uknj['stanovi_uknjizeno'] = self.cursor.fetchall()
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND uknjizeno IS NOT TRUE")
#         uknj['stanovi_neuknjizeno'] = self.cursor.fetchall()
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'kuca' AND uknjizeno IS TRUE")
#         uknj['kuce_uknjizeno'] = self.cursor.fetchall()
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'kuca' AND uknjizeno IS NOT TRUE")
#         uknj['kuce_neuknjizeno'] = self.cursor.fetchall()
#         return uknj
        
#     def najskuplje(self):
#         self.cursor.execute("SELECT id, naslov, cena, grad, kvadratura, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE ponuda = 'P' and tip = 'stan' ORDER BY cena DESC LIMIT 30")
#         najskuplji_stanovi = self.cursor.fetchall()
#         self.cursor.execute("SELECT id, naslov, cena, grad, kvadratura, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE ponuda = 'P' and tip = 'kuca' ORDER BY cena DESC LIMIT 30")
#         najskuplje_kuce = self.cursor.fetchall()
#         return {
#             'najskuplji_stanovi': najskuplji_stanovi,
#             'najskuplje_kuce': najskuplje_kuce,
#         }
        
#     def najvece(self):
#         self.cursor.execute("SELECT id, naslov, kvadratura, ponuda, cena, grad, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'stan' ORDER BY kvadratura DESC LIMIT 100")
#         najveci_stanovi = self.cursor.fetchall()
#         self.cursor.execute("SELECT id, naslov, kvadratura, ponuda, cena, grad, stanje, godina_izgradnje, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'kuca' ORDER BY kvadratura DESC LIMIT 100")
#         najvece_kuce = self.cursor.fetchall()
#         return {
#             'najveci_stanovi': najveci_stanovi,
#             'najvece_kuce': najvece_kuce,
#         }

#     def cene_2020(self):
#         self.cursor.execute("SELECT id, cena, naslov, grad, kvadratura FROM nekretnine WHERE godina_izgradnje = '2020' AND ponuda = 'P' ORDER BY cena DESC")
#         prodaja = self.cursor.fetchall()
#         self.cursor.execute("SELECT id, cena, naslov, grad, kvadratura FROM nekretnine WHERE godina_izgradnje = '2020' AND ponuda = 'I' ORDER BY cena DESC")
#         izdavanje = self.cursor.fetchall()
#         return {
#             'prodaja': prodaja,
#             'izdavanje': izdavanje,
#         }
        
#     def top_broj_soba(self):
#         self.cursor.execute("SELECT id, broj_soba, tip, naslov, cena, grad, kvadratura, broj_soba, broj_kupatila FROM nekretnine ORDER BY broj_soba DESC LIMIT 30")
#         return self.cursor.fetchall()
        
#     def top_kvadratura_stanovi(self):
#         self.cursor.execute("SELECT id, kvadratura, naslov, cena, grad, broj_soba, broj_kupatila FROM nekretnine WHERE tip = 'stan' ORDER BY kvadratura DESC LIMIT 30")
#         return self.cursor.fetchall()
    
#     def top_povrsina_zemljista(self):
#         self.cursor.execute("SELECT id, povrsina_zemljista, naslov, cena, kvadratura, grad FROM nekretnine ORDER BY povrsina_zemljista DESC LIMIT 30")
#         return self.cursor.fetchall()

#     def top_delovi_beograda(self):
#         self.cursor.execute("SELECT deo_grada, COUNT(*) AS broj_nekretnina FROM nekretnine WHERE grad = 'Beograd' GROUP BY deo_grada ORDER BY broj_nekretnina DESC LIMIT 10")
#         return self.cursor.fetchall()
    
#     def broj_nekretnina_u_beogradu(self):
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE grad = 'beograd'")
#         return self.cursor.fetchone()['broj']
    
#     def kategorije_kvadrature(self):
#         kategorije = {}
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura <= 35")
#         kategorije['do_35'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 35 AND kvadratura <= 50")
#         kategorije['36-50'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 51 AND kvadratura <= 65")
#         kategorije['51-65'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 66 AND kvadratura <= 80")
#         kategorije['66-80'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 81 AND kvadratura <= 95")
#         kategorije['81-95'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 96 AND kvadratura <= 110")
#         kategorije['96-110'] = self.cursor.fetchone()['broj']
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P' AND kvadratura > 110")
#         kategorije['od_111'] = self.cursor.fetchone()['broj']
#         return kategorije
    
#     def broj_stanova_za_prodaju(self):
#         self.cursor.execute("SELECT COUNT(*) AS broj FROM nekretnine WHERE tip = 'stan' AND ponuda = 'P'")
#         return self.cursor.fetchone()['broj']
        
#     def nekretnine_po_dekadama(self):
#         nekretnine = {}
#         prepared_statement = "SELECT COUNT(*) AS broj FROM nekretnine WHERE godina_izgradnje >= %s AND godina_izgradnje <= %s"
#         dekade = [(1951, 1960), (1961, 1970), (1971, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2020)]
#         for d in dekade:
#             self.cursor.execute(prepared_statement, d)
#             nekretnine[str(d)] = self.cursor.fetchone()['broj']
#         return nekretnine