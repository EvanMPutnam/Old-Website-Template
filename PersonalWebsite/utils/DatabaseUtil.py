import sqlite3



conn = sqlite3.connect("../database.db")
c = conn.cursor()
c.execute('''SELECT content from blog_post''')

file = open("markdown.txt", "w+")
for i in c.fetchall():
    print(i)
    file.write(i[0])

