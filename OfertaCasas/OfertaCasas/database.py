import sqlite3

conn = sqlite3.connect('TuCasaAlFin.db')
curr = conn.cursor()


class Database:
    def __init__(self):
        self.conn = sqlite3
        self.curr = None

    def connection(self, dbname):
        self.conn.connect(dbname)
        self.curr = self.conn.cursor()
        pass

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS DataHouses""")
        self.curr.execute("""
            CREATE TABLE DataHouses(
            url = text,
            location = text,
            category = text,
            bedrooms = integer,
            toilets = integer,
            sets = text,
            price = real
            )
        """)

    def store_db(self, row_tuple):
        self.curr.execute("""
            insert into DataHouses values (?,?,?,?,?,?,?)
        """, row_tuple)
        self.conn.commit()

