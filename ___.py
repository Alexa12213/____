import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

conn = sqlite3.connect('weather_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time DATETIME,
        temperature TEXT
    )
''')
conn.commit()
url = 'https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    temperature_element = soup.select_one('.temperature .p1').text.strip()
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO weather_data (date_time, temperature) VALUES (?, ?)', (current_datetime, temperature_element))
    conn.commit()
    print(f"Дані успішно записано: {current_datetime}, Температура: {temperature_element}")
else:
    print(f"Помилка: Неможливо отримати дані з {url}. Код статусу: {response.status_code}")