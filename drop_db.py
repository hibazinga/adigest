import sqlite3
def init_db():
    con = sqlite3.connect('/tmp/common.db')
    cur = con.cursor()
    cur.executescript("""
    drop table user;
    drop table whitelist;
    drop table email;
    drop table lastdigest;
    drop table userclick;
    """)

if __name__ == "__main__":
    init_db()

