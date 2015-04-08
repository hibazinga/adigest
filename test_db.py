import sqlite3
import db
import settings

def init_db():
    con = sqlite3.connect(settings._DB)
    cur = con.cursor()
    '''
    db.insert_user(cur,'12345a','renyb@qq.com', 'Yanbin','Ren', '5a5a5a5a5a5',2,143331313)
    db.insert_user(cur,'12345b','xieyu@qq.com', 'Yu','Xie', '6dwqbuy171',6,146387654)
    db.insert_user(cur,'12345c','kaiwang@qq.com', 'kay','Wang', '78yqehdq',1,143331314)
    
    db.delete_user(cur, 'kaiwang@qq.com')
    con.commit()

    
    db.insert_whitelist(cur, 'renyb@qq.com', 'hello')
    cur.execute("select * from whitelist")
    data = cur.fetchall()
    for i in data:
        print i

    db.delete_whitelist(cur,'renyb@qq.com', 'hello')
    db.delete_whitelist(cur,'renyb@qq.com', 'a@amazon.com')
    aaa = db.get_whitelist(cur,'renyb@qq.com')
    for i in aaa:
        print "###",i

    db.update_user_preference(cur, 'renyb@qq.com', 100)
    cur.execute("select * from user")
    data = cur.fetchall()
    for i in data:
        print i

    cur.execute("select * from lastdigest")
    data = cur.fetchall()
    for i in data:
        print i


    db.update_lastdigest(cur, 'renyb', 140000000)
    cur.execute("select * from lastdigest")
    data = cur.fetchall()
    for i in data:
        print i
#db.insert_email(cur, 'renyb@qq.com','7y781d871g','7831gd8g3', 'a@amazon.com', 'Amazon', 142230303, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADs', 0)

    cur.execute("select * from email")
    data = cur.fetchall()
    for i in data:
        print i
    con.commit()
    data = db.get_digest_list(cur, 'renyb@qq.com')
    for i in data:
        print i
    cur.execute("select * from lastdigest")
    data = cur.fetchall()
    for i in data:
        print i

    db.insert_email(cur, 'renyb@qq.com','7y781d871g2','227831gd8g3', 'a@amazon.com', 'Amazon', 142230303, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADs', 0)
    db.insert_email(cur, 'renyb@qq.com','18ydh18dhd87','2dj1dh137d831h', 'a@gap.com', 'Gap', 143303030, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADyd1728y1s', 0)
    db.insert_email(cur, 'renyb@qq.com','d1hd1dh821','2d1n28d7h81', 'b@facebook.com', 'facebook', 142430303, 'http://www.baidu.com', 'http://pic.baidu.com', 'AD2189u81s', 0)
    db.insert_email(cur, 'renyb@qq.com','d31dh1387hd8','d21h87d1hd', 'a@gmail.com', 'Gmail', 145510391, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADd1hd81s', 0)
    
    db.insert_email(cur, 'zjuxie@gmail.com','d31dh1387hd9','2d1h87d1hd2', 'a@gmail.com', 'Gmail', 145510391, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADd1hd81s', 0)
    db.insert_email(cur, 'zjuwangk@gmail.com','d31dh1387hd10','2d1h87d1hd3', 'a@gmail.com', 'Gmail', 145510391, 'http://www.baidu.com', 'http://pic.baidu.com', 'ADd1hd81s', 0)
    '''
    cur.execute("select * from whitelist")
    data = cur.fetchall()
    for i in data:
        print i
    con.commit()
    cur.close()
    con.close()
if __name__ == "__main__":
    init_db()

'''
    cur.execute("insert into user values ('12345a','Yanbin','Ren','renyb@qq.com','5a5a5a5a5a5',2,143331313)")
    cur.execute("insert into user values ('12345b','Yu','Xie','xieyu@qq.com','5adqwhuyqq',6,143331211)")
'''