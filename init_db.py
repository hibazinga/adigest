import sqlite3
def init_db():
    con = sqlite3.connect('/tmp/common.db')
    cur = con.cursor()
    '''
        preference: 
                    1 12 hrs
                    2 1 day
                    6 3 days
                    14 1 wk
    '''
    cur.executescript("""
    create table user(
        uid varchar unique,
        first_name varchar,
        last_name varchar,
        email varchar primary key,
        token varchar,
        preference integer,
        timestamp integer
    );
    
    create table whitelist(
        email varchar primary key,
        sender varchar
    );

    create table email(
        email_addr varchar,
        email_id varchar,
        gmail_message_id varchar,
        sender_email varchar,
        sender_name varchar,
        timestamp integer,
        unsub_url varchar,
        pic_url varchar,
        subject varchar,
        category integer
    );
    
    create table lastdigest(
        email varchar primary key,
        timestamp integer
    );
    
    create table userclick(
        email varchar,
        sender_name varchar,
        click integer
    );
    """)

if __name__ == "__main__":
    init_db()

