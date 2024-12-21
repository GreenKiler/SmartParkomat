import streamlit as st
import pyodbc

# Połączenie z bazą danych Azure SQL
def get_connection():
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:smart-parkomat.database.windows.net;Database=smart-parkomat-db;Uid=SmartAdmin;Pwd=Parkomat123!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return conn

# Wprowadzanie numeru rejestracyjnego
st.title("Dodaj numer rejestracyjny")
plate_number = st.text_input("Podaj numer tablicy rejestracyjnej")

if st.button("Dodaj do bazy"):
    if plate_number:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO plates (plate_number) VALUES (?)", (plate_number,))
        conn.commit()
        conn.close()
        st.success(f"Numer {plate_number} został dodany do bazy danych.")
    else:
        st.error("Proszę wprowadzić numer tablicy rejestracyjnej.")
