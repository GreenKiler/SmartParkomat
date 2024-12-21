import sqlite3

# Połączenie z bazą danych
connection = sqlite3.connect("plates.db")
cursor = connection.cursor()

# Tworzenie tabeli
cursor.execute('''
CREATE TABLE IF NOT EXISTS plates (
    id INTEGER PRIMARY KEY,
    plate_number TEXT NOT NULL
)
''')

# Dodawanie przykładowych danych
cursor.execute("INSERT INTO plates (plate_number) VALUES ('ABC123')")
cursor.execute("INSERT INTO plates (plate_number) VALUES ('XYZ789')")
connection.commit()
connection.close()