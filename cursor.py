#SQLite к сожалению не позволяет явно задавать переменные, поэтому не смог сделать
# рекурсивную выборку юзеров

import sqlite3

connect = sqlite3.connect("inst_parse.db")
cur = connect.cursor()

cur.execute("DELETE FROM instafollow WHERE NOT EXISTS (SELECT * FROM instafollowed i2 WHERE instafollow.follow_name = i2.followed_name AND instafollow.user_name = i2.user_name;")
connect.commit()

cur.execute("DELETE FROM instafollow2 NOT EXISTS (SELECT * FROM instafollowed2 i22 WHERE instafollow2.follow_name2 = i22.followed_name2 AND instafollow2.user_name2 = i22.user_name2);")
connect.commit()

var1 = """SELECT follow_name FROM (SELECT i.follow_name, i.follow_depth, i2.follow_name2, i2.follow_depth2
FROM Instafollow as i INNER JOIN Instafollow2 as i2 ON i.follow_name = i2.follow_name2
ORDER BY follow_depth+follow_depth2 LIMIT 1)"""

var2 = """SELECT instafollow.user_name FROM instafollow WHERE instafollow.follow_name = 
(SELECT follow_name FROM (""" + var1 + ")) ORDER BY user_depth LIMIT 1"

var3 = """SELECT user_name FROM instafollow WHERE follow_name = (""" + var2 + ") ORDER BY user_depth LIMIT 1"

var4 = """SELECT user_name FROM instafollow WHERE follow_name = (""" + var3 + ")"

var5 = """SELECT instafollow2.user_name2 FROM instafollow2 WHERE instafollow2.follow_name2 = 
(SELECT follow_name FROM (""" + var1 + ")) ORDER BY user_depth LIMIT 1"

var6 = """SELECT user_name2 FROM instafollow2 WHERE follow_name2 = (""" + var5 + ") ORDER BY user_depth LIMIT 1"

var7 = """SELECT user_name2 FROM instafollow2 WHERE follow_name2 = (""" + var6 + ")"

cur.execute(var4)
null_result = cur.fetchone()
if null_result:
    print(null_result)

cur.execute(var3)
first_result = cur.fetchone()
if first_result:
    print(first_result)

cur.execute(var2)
second_result = cur.fetchone()
if second_result:
    print(second_result)

cur.execute(var1)
fourth_result = cur.fetchone()
if fourth_result:
    print(fourth_result)

cur.execute(var5)
fifth_result = cur.fetchone()
if fifth_result:
    print(fifth_result)

cur.execute(var6)
sixth_result = cur.fetchone()
if sixth_result:
     print(sixth_result)

cur.execute(var7)
seventh_result = cur.fetchone()
if seventh_result:
     print(seventh_result)

connect.close()