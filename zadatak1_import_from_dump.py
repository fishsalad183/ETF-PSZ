from db.db import MysqlDAO

DUMP_FILE = "db\Dump20220602.sql"

db = MysqlDAO()
db.import_database_from_dump(DUMP_FILE)
db.close() 