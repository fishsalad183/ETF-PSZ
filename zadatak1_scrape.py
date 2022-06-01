# Run from the Makefile as 'make scrape'!

from db.db import MysqlDAO
from scraper.run_scraper import Scraper

try:
    db = MysqlDAO()
    db.create_database()
    db.create_table()

    scraper = Scraper()
    scraper.run_spiders()
finally:
    db.close()