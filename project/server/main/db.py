import sqlite3

class Bookmark():
    def __init__(self, link, title, tags):
        self.link = link
        self.title = title
        self.tags = tags.split(',')

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.setup_tables()

    def setup_tables(self):
        cursor = self.conn.cursor()
        command = """CREATE TABLE IF NOT EXISTS bookmarks(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            LINK text, 
            TITLE text,
            TAGS text)
        """
        cursor.execute(command)

    def add_link(self, link, title, tags):
        cursor = self.conn.cursor()
        command = f"INSERT INTO bookmarks(LINK, TITLE, TAGS) values(?, ?, ?)"
        cursor.execute(command, (link, title, ','.join(tags)))
        self.conn.commit()

    def get_links(self):
        cursor = self.conn.cursor()
        command = "SELECT LINK, TITLE, TAGS from bookmarks"
        cursor.execute(command)
        data = cursor.fetchall()
        return [Bookmark(d[0], d[1], d[2].split(',')) for d in data]
