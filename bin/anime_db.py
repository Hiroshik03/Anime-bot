import sqlite3
import parser_anime
async def db_init():
    connection = sqlite3.connect('anime.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Anime (
    year INTEGER,
    name TEXT NOT NULL PRIMARY KEY,
    png TEXT NOT NULL,
    raiting TEXT NOT NULL,
    url TEXT NOT NULL,
    trailer TEXT,
    genre TEXT,
    description TEXT,
    series TEXT,
    fullDescription TEXT
    )
    ''')
    connection.commit()
    connection.close()
async def anime_on_year_set(data,year):
    await db_init()
    connection = sqlite3.connect('anime.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Anime WHERE year=?',[year])
    for anime in data:
        cursor.execute('INSERT INTO Anime (year, name, png, raiting, url, genre,description) VALUES (?,?,?,?,?,?,?)', (year,anime[0],anime[2],anime[3],anime[1],anime[5],anime[4] ))
        connection.commit()
    connection.commit()
    connection.close()
async def anime_on_genre(genre):
    connection = sqlite3.connect('anime.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Anime WHERE genre LIKE ?', ['%' + genre + '%'])
    anime = cursor.fetchall()
    return anime
async def anime_on_year(year):
    connection = sqlite3.connect('anime.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Anime WHERE year =?', [year])
    anime = cursor.fetchall()
    if len(anime) == 0:
        try:
            await parser_anime.data_reader_on_year(year)
        except:
            return "По запросу не нашлось аниме"
    return anime
