import sqlite3

connection = sqlite3.connect('Kurs_qushish.db')

cursor = connection.cursor()

def main():
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS kurs_qushish(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kurs_nomi VARCHAR(50),
        kurs_narxi INTEGER,
        toliq_malumot TEXT,
        oqituvchi_haqida TEXT
)
"""
)
connection.commit()

#print(cursor.execute("SELECT * FROM kurs_qushish").fetchall())

def kurs_qoshish_func(*args):
    """
    args - bu funksiya qabul qilayotgan foydalanuvchi ma'lumotlar to'plami
    """
    sql = """INSERT INTO kurs_qushish(kurs_nomi,kurs_narxi,toliq_malumot,oqituvchi_haqida)
            VALUES(?,?,?,?)"""
    cursor.execute(sql,args)
    connection.commit()
    

if __name__ == "__main__":
    main()