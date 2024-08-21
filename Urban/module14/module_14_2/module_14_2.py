import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
    """
)

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users(email)")

for i in range(1, 11):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", 10 * i, 1000))

for i in range(1, 11):
    if i % 2 != 0:
        cursor.execute("UPDATE Users SET balance = ? WHERE username = ?",
                       (500, f"User{i}"))

for i in range(1, 11):
    if i % 3 == 1:
        cursor.execute("DELETE FROM Users WHERE username = ?",
                       (f"User{i}",))


# addition to code from module_14_1
cursor.execute("DELETE FROM Users WHERE id = 6")
cursor.execute("SELECT COUNT(id) FROM Users")
total_users = cursor.fetchone()[0]
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

connection.commit()
connection.close()
